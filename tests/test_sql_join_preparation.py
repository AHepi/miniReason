import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from minireason import sql_join_preparation as prep

class SQLPreparationTests(unittest.TestCase):
    def test_equal_visible_inputs_need_distinct_successors(self):
        w=prep.ambiguity_witness()
        self.assertEqual(w["oracle"][0]["snapshots"][0],w["oracle"][1]["snapshots"][0])
        self.assertEqual(w["histories"][0]["events"],w["histories"][1]["events"])
        self.assertEqual(w["oracle"][0]["snapshots"][1],[{"row":[1,7,"x"],"multiplicity":1}])
        self.assertEqual(w["oracle"][1]["snapshots"][1],[
            {"row":[1,7,"x"],"multiplicity":1},{"row":[1,7,None],"multiplicity":1}])

    def test_real_null_and_padded_null_have_different_future_uses(self):
        result=prep.run_case(prep.cases()[1])["snapshots"]
        # Deleting the last real NULL row changes underlying state while preserving view.
        self.assertEqual(result[0],result[2])
        self.assertEqual(result[2],result[3])
        # Two real NULL-valued partners produce two visible rows, not one.
        self.assertEqual(result[5],[{"row":[1,7,None],"multiplicity":2}])
        self.assertEqual(result[6],[{"row":[1,7,None],"multiplicity":1}])

    def test_duplicate_multiplicity_and_last_match_restoration(self):
        result=prep.run_case(prep.cases()[0])["snapshots"]
        self.assertEqual(result[2],[{"row":[1,7,"x"],"multiplicity":2}])
        self.assertEqual(result[3],[{"row":[1,7,"x"],"multiplicity":1}])
        self.assertEqual(result[4],result[0])

    def test_null_keys_never_join_under_equality(self):
        result=prep.run_case(prep.cases()[2])["snapshots"]
        self.assertEqual(result[0],result[1])
        self.assertEqual(result[1],result[2])
        for snapshot in result:
            self.assertTrue(all(x["row"][2] is None for x in snapshot if x["row"][1] is None))

    def test_multiple_left_rows_preserve_separate_multiplicities(self):
        result=prep.run_case(prep.cases()[3])["snapshots"]
        self.assertEqual(sum(x["multiplicity"] for x in result[2]),6)
        self.assertEqual(sum(x["multiplicity"] for x in result[3]),3)
        self.assertEqual(sum(x["multiplicity"] for x in result[4]),2)
        self.assertEqual(result[5],[])

    def test_independent_key_events_commute_and_preserve_other_output(self):
        initial={"L":[[1,7],[2,9]],"R":[]}
        a=prep.event("insert","R",10,7,"x")
        b=prep.event("insert","R",11,9,"y")
        one=prep.run_case({"case_id":"a","initial":initial,"events":[a,b]})["snapshots"]
        two=prep.run_case({"case_id":"b","initial":initial,"events":[b,a]})["snapshots"]
        self.assertEqual(one[-1],two[-1])
        self.assertEqual([x for x in one[0] if x["row"][0]==2],
                         [x for x in one[1] if x["row"][0]==2])

    def test_recode_preserves_every_output_bag_under_mapping(self):
        for case in prep.cases():
            original=prep.run_case(case)["snapshots"]
            recoded=prep.run_case(prep.recode_case(case))["snapshots"]
            for old,new in zip(original,recoded,strict=True):
                expected=[{"row":[x["row"][0]+1000,
                    None if x["row"][1] is None else x["row"][1]+10000,
                    None if x["row"][2] is None else "r:"+x["row"][2]],
                    "multiplicity":x["multiplicity"]} for x in old]
                self.assertEqual(sorted(expected,key=prep.canonical),sorted(new,key=prep.canonical))

    def test_finite_recode_rejects_signed32_overflow(self):
        for initial in ({"L":[[2**31-1,7]],"R":[]},
                        {"L":[[1,2**31-1]],"R":[]}):
            with self.assertRaisesRegex(ValueError,"ID_DOMAIN|KEY_DOMAIN"):
                prep.recode_case({"case_id":"outside_bank","initial":initial,"events":[]})

    def test_delete_requires_exact_existing_before_image(self):
        db=prep.connect({"L":[[1,7]],"R":[[10,7,"x"]]})
        try:
            for row in ([99,7,"x"],[10,8,"x"],[10,7,None]):
                with self.assertRaisesRegex(ValueError,"DELETE_BEFORE_IMAGE"):
                    prep.apply_event(db,prep.event("delete","R",*row))
            self.assertEqual(prep.view(db),[{"row":[1,7,"x"],"multiplicity":1}])
        finally:
            db.close()

    def test_domain_excludes_bool_mixed_types_and_implicit_ids(self):
        for row in ([True,7],[1,"7"],[None,7],[2**31,7]):
            with self.assertRaises(ValueError):
                prep.connect({"L":[row],"R":[]})
        with self.assertRaises(sqlite3.IntegrityError):
            prep.connect({"L":[[1,7],[1,9]],"R":[]})

    def test_material_allowlist_cannot_include_operator_outputs(self):
        bundle=prep.make_bundle()
        allow=bundle["operator/route-status.json"]["participant_allowlist"]
        self.assertEqual(allow,["participant/construction.json"])
        self.assertFalse(any(key in bundle[allow[0]] for key in ("histories","oracle","snapshots","needed_distinction")))
        self.assertEqual(bundle["operator/route-status.json"]["provider_calls"],0)
        self.assertIsNone(bundle["operator/route-status.json"]["candidate_occurrence"])

    def test_bundle_is_deterministic_and_refuses_overwrite(self):
        self.assertEqual(prep.make_bundle(),prep.make_bundle())
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/"bundle"
            prep.write_bundle(path)
            old=(path/"manifest.json").read_bytes()
            with self.assertRaises(FileExistsError):
                prep.write_bundle(path)
            self.assertEqual((path/"manifest.json").read_bytes(),old)

if __name__=="__main__":
    unittest.main()
