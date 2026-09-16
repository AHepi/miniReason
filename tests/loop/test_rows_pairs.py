"""Offline pair custody/admission checks; no calls, initialization or Git fixtures."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from minireason.loop import rows_pairs as pairs
from minireason.loop.surface import resolve_unique, within_declared_span

ROOT = Path(__file__).resolve().parents[2]
F09 = ROOT / "experiments/diagnostics/F001-fork5-multifamily/occurrence-09"


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def fixture():
    """All F003 treatment groups as an in-memory native occurrence; no temp IO."""
    occurrence = ROOT / "work/w11/fixture"
    mapping = []
    for arm, code in (("mini_prose", "p"), ("matched", "m")):
        for label, mark, prefix, objection in (
                ("RETURNED", "R", "ret", "objection"),
                ("ARCHIVED", "A", "arc", "objection"),
                ("RECODING", "E", "rec", "rec_objection"),
                ("CHANGED", "D", "chg", "chg_objection"),
                ("CARRIER", "C", "car", "car_objection")):
            mapping.append(dict(arm=arm, code=code + mark, treatment=label,
                                objection_node=objection, rival_node="rival",
                                response_node=prefix + "_response",
                                carry_node=prefix + "_carry",
                                route="archive-context" if label == "ARCHIVED" else "returned"))
    data = {occurrence / "material.json": encoded({
        "pair_rows": {"source_tag": "d", "problem": "daily", "cycle": 1, "groups": mapping}})}

    def coord(arm, node):
        return dict(problem="daily", arm=arm, cycle=1, node=node)

    def path(kind, arm, node, suffix):
        return occurrence / kind / "daily" / arm / "cycle01" / (node + suffix)

    def add(arm, node, text):
        raw = text.encode("utf-8")
        data[path("responses", arm, node, ".txt")] = raw
        data[path("artifacts", arm, node, ".json")] = encoded({
            "coordinate": coord(arm, node), "artifact_id": "synthetic-" + node,
            "public_text_sha256": sha(raw)})

    for arm in ("mini_prose", "matched"):
        for node in ("account", "objection", "rival", "rec_objection", "chg_objection", "car_objection"):
            add(arm, node, "Earlier " + node + " caf\u00e9\r\nFrozen target.\r\n")
    for group in mapping:
        arm = group["arm"]
        response, carry = group["response_node"], group["carry_node"]
        add(arm, response, "The rival keeps consent.\r\n" +
            ("The objection corrects caf\u00e9 timings.\r\n" if group["treatment"] != "ARCHIVED" else
             "No criticism was delivered.\r\n"))
        add(arm, carry, "The selected response supplies caf\u00e9 timings.\r\n")
        for later, predecessors in ((response, ["rival"] +
                  ([] if group["treatment"] == "ARCHIVED" else [group["objection_node"]])),
                  (carry, [response])):
            projections = []
            for node in predecessors:
                projections.append({"artifact_id": "synthetic-projection",
                    "selected_source": {"source": node, "coordinate": coord(arm, node),
                    "artifact_id": "synthetic-" + node, "absent": False, "view": "both",
                    "public_text_sha256": sha(data[path("responses", arm, node, ".txt")])}})
            visible = [p["selected_source"] for p in projections]
            brief = "synthetic fixture"
            if arm == "matched":
                brief = "\n\n".join("## Selected input " + s["source"] +
                    "\n\nSource " + s["source"] + ": " + pairs._coord_key(s["coordinate"]) +
                    "; selected view: both\nArtifact: " + s["artifact_id"] + "\n"
                    for s in visible)
            data[path("traces", arm, later, ".json")] = encoded({
                "coordinate": coord(arm, later),
                "projection_artifacts": [] if arm == "matched" else projections,
                "visible_sources": visible,
                "rendering": "direct_explicit_views" if arm == "matched" else "canonical_compile_reducer_render",
                "template_id": "f003", "original_brief": brief,
                "original_brief_sha256": sha(brief.encode("utf-8"))})
    return occurrence, data


class RowsPairsTests(unittest.TestCase):
    def build_fixture(self, data=None):
        occurrence, base = fixture()
        data = base if data is None else data
        def read(path):
            if path not in data:
                raise FileNotFoundError(str(path))
            return data[path]
        with patch.object(Path, "read_bytes", read), \
             patch.object(Path, "is_file", lambda path: path in data):
            return pairs.build_rows(occurrence, repo_root=ROOT)

    def test_real_occurrence_six_candidate_slots_with_exact_evidence(self):
        rows = pairs.build_rows(F09, repo_root=ROOT)
        self.assertEqual([r["row_key"] for r in rows], [
            "h005-row/pr#u/ref/o", "h005-row/pr#u/ref/v", "h005-row/pc#u/ref/r",
            "h005-row/fr#u/ref/o", "h005-row/fr#u/ref/v", "h005-row/fc#u/ref/r"])
        self.assertEqual([r["admission"] for r in rows], ["ADMITTED"] * 6)
        for row in rows:
            self.assertTrue(row["referring_passages"])
            for ref in row["referring_passages"]:
                for key in ("reference", "passage"):
                    source = ref[key]
                    raw = (ROOT / source["path"]).read_bytes()
                    self.assertEqual(sha(raw), source["sha256"])
                    self.assertEqual(raw[source["byte_start"]:source["byte_end"]],
                                     source["text"].encode("utf-8"))
                    self.assertEqual(raw[:source["byte_start"]].count(b"\n") + 1,
                                     source["line_start"])
        self.assertIn("the objection lands on sequencing and cost", rows[0]["referring_passages"][0]["passage"]["text"])
        self.assertTrue(any("edd651259f4dd1e6" in r["reference"]["text"]
                            for r in rows[2]["referring_passages"]))

    def test_synthetic_f003_treatments_share_positions_not_evidence(self):
        rows = self.build_fixture()
        self.assertEqual(len(rows), 30)
        unresolved = [r for r in rows if r["admission"] == "UNRESOLVED"]
        self.assertEqual(len(unresolved), 2)
        self.assertTrue(all(r["treatment"] == "ARCHIVED" and
                            r["pair_position"] == "objection->response" for r in unresolved))
        self.assertEqual({r["comparison_position"] for r in rows}, {"or", "vr", "rc"})
        self.assertEqual({r["treatment"] for r in rows},
                         {"RETURNED", "ARCHIVED", "RECODING", "CHANGED", "CARRIER"})

    def test_missing_reference_does_not_become_absence(self):
        occurrence, data = fixture()
        p = occurrence / "responses/daily/mini_prose/cycle01/ret_response.txt"
        data[p] = b"A correct-looking answer without a referring passage."
        artifact_path = occurrence / "artifacts/daily/mini_prose/cycle01/ret_response.json"
        artifact = json.loads(data[artifact_path])
        artifact["public_text_sha256"] = sha(data[p])
        data[artifact_path] = encoded(artifact)
        rows = self.build_fixture(data)
        self.assertEqual(rows[0]["admission"], "UNRESOLVED")
        self.assertIn("exact referring passage", rows[0]["reason"])
        self.assertNotIn("absent", rows[0]["reason"])

    def test_wrong_source_hash_and_ambiguous_trace_refuse(self):
        occurrence, data = fixture()
        p = occurrence / "traces/daily/mini_prose/cycle01/ret_response.json"
        trace = json.loads(data[p])
        trace["projection_artifacts"][1]["selected_source"]["public_text_sha256"] = "0" * 64
        data[p] = encoded(trace)
        self.assertIn("custody mismatch", self.build_fixture(data)[0]["reason"])
        trace["projection_artifacts"].append(trace["projection_artifacts"][1])
        data[p] = encoded(trace)
        self.assertIn("not uniquely mapped", self.build_fixture(data)[0]["reason"])

    def test_archive_context_is_not_a_guard_target(self):
        row = self.build_fixture()[3]
        self.assertEqual(row["admission"], "UNRESOLVED")
        surface = pairs.build_surface(row)
        self.assertIn(b"ARCHIVE CONTEXT ONLY", surface.text)
        offset = resolve_unique(surface, row["target"]["text"])
        self.assertIsNotNone(offset)
        self.assertFalse(within_declared_span(surface, offset))
        self.assertTrue(all(s.side != "pair-target" for s in surface.spans))

    def test_raw_byte_fidelity_and_codepoint_correspondence(self):
        for row in [*pairs.build_rows(F09, repo_root=ROOT), *self.build_fixture()]:
            surface = pairs.build_surface(row)
            for source in (row["referring"], row["target"], *row["context"]):
                self.assertIn(source["text"].encode("utf-8"), surface.text)
            for span in surface.spans:
                source = next(s for s in (row["referring"], row["target"])
                              if s["path"] == span.occurrence_path)
                self.assertEqual(surface.text[span.start:span.end], source["text"].encode("utf-8"))
                self.assertEqual(span.source_field, "raw_utf8_text")
        row = self.build_fixture()[0]
        surface = pairs.build_surface(row)
        quote = "The objection corrects caf\u00e9 timings."
        offset = resolve_unique(surface, quote)
        self.assertTrue(within_declared_span(surface, offset))
        source = pairs.raw_offset(row, offset)
        self.assertEqual(source["text"], quote)
        self.assertNotEqual(source["byte_end"], source["codepoint_end"])
        self.assertIsNone(offset.source_field)

    def test_keys_injective_and_windows_bound(self):
        rows = [*pairs.build_rows(F09, repo_root=ROOT), *self.build_fixture()]
        pairs.validate_keys(rows)
        self.assertEqual(len(pairs.adapter_index(rows)), len(rows))
        self.assertEqual(max(len(p) for r in rows for p in pairs.provider_paths(r["row_key"]).values()), 193)
        with self.assertRaisesRegex(ValueError, "collision"):
            pairs.validate_keys([rows[0], rows[0]])
        with self.assertRaisesRegex(ValueError, "Windows"):
            pairs.validate_keys(rows, run_name="x" * 150)

    def test_later_byte_custody_is_required(self):
        occurrence, data = fixture()
        data[occurrence / "responses/daily/mini_prose/cycle01/ret_response.txt"] += b"changed"
        self.assertIn("hash mismatch", self.build_fixture(data)[0]["reason"])

    def test_coordinate_traversal_refused_before_source_read(self):
        occurrence, data = fixture()
        material = json.loads(data[occurrence / "material.json"])
        material["pair_rows"]["groups"][0]["response_node"] = "../../outside"
        data[occurrence / "material.json"] = encoded(material)
        with self.assertRaisesRegex(ValueError, "unsafe pair coordinate"):
            self.build_fixture(data)
        with patch.object(Path, "read_bytes", side_effect=AssertionError("read escaped root")):
            with self.assertRaises(ValueError):
                pairs.build_rows(ROOT.parent / "outside", repo_root=ROOT)

    def test_final_f003_topology_missing_rival_stays_unresolved(self):
        occurrence, data = fixture()
        data = {path: content for path, content in data.items()
                if path.stem not in ("rival", "account")}
        rows = self.build_fixture(data)
        self.assertEqual(sum(r["admission"] == "UNRESOLVED" for r in rows), 12)
        rivals = [r for r in rows if r["pair_position"] == "rival->response"]
        self.assertEqual(len(rivals), 10)
        self.assertTrue(all(r["admission"] == "UNRESOLVED" for r in rivals))

    def test_same_position_juxtaposition_keeps_five_distinct_surfaces(self):
        groups = pairs.juxtapose(self.build_fixture())
        self.assertEqual(len(groups), 6)
        for group in groups:
            candidates = group["candidates"]
            self.assertEqual([c["treatment"] for c in candidates],
                             ["RETURNED", "ARCHIVED", "RECODING", "CHANGED", "CARRIER"])
            self.assertEqual(len({c["surface"].digest for c in candidates}), 5)
        self.assertEqual(groups[0]["candidates"][1]["admission"], "UNRESOLVED")

    def record_fixture(self, record_id="o1", duplicate=False):
        occurrence, data = fixture()
        target = occurrence / "responses/daily/mini_prose/cycle01/objection.txt"
        later = occurrence / "responses/daily/mini_prose/cycle01/ret_response.txt"
        data[target] = encoded({"records": [{"id": "o1", "text": "Frozen correction"}]
                                          * (2 if duplicate else 1)})
        token = "h005.f003.p.ret_response.0#" + record_id
        data[later] = encoded({"mentions": [token]})
        for node, source in (("objection", target), ("ret_response", later)):
            path = occurrence / "artifacts/daily/mini_prose/cycle01" / (node + ".json")
            artifact = json.loads(data[path])
            artifact["public_text_sha256"] = sha(data[source])
            data[path] = encoded(artifact)
        path = occurrence / "traces/daily/mini_prose/cycle01/ret_response.json"
        trace = json.loads(data[path])
        trace["original_brief"] = "## Selected input objection (p.ret_response.0)"
        trace["projection_artifacts"][1]["selected_source"]["public_text_sha256"] = sha(data[target])
        data[path] = encoded(trace)
        return data

    def test_named_record_suffix_is_not_laundered_to_whole_contribution(self):
        row = self.build_fixture(self.record_fixture("missing"))[0]
        self.assertEqual(row["admission"], "UNRESOLVED")
        self.assertEqual(row["referring_passages"], [])
        self.assertEqual(len(row["unresolved_references"]), 1)
        self.assertIn("#missing", row["unresolved_references"][0]["reference"]["text"])

    def test_duplicate_named_record_id_is_unresolved(self):
        row = self.build_fixture(self.record_fixture(duplicate=True))[0]
        self.assertEqual(row["admission"], "UNRESOLVED")
        self.assertEqual(len(row["unresolved_references"]), 1)

    def test_unique_authored_record_anchor_keeps_exact_raw_span(self):
        row = self.build_fixture(self.record_fixture())[0]
        self.assertEqual(row["admission"], "ADMITTED")
        reference = row["referring_passages"][0]
        self.assertEqual(reference["target_record_id"], "o1")
        anchor = reference["target_anchor"]
        self.assertEqual(anchor["text"], '"id": "o1"')
        self.assertEqual(row["target"]["text"].encode("utf-8")[anchor["byte_start"]:anchor["byte_end"]],
                         anchor["text"].encode("utf-8"))

    def test_duplicate_source_pair_under_distinct_codes_refused(self):
        occurrence, data = fixture()
        material = json.loads(data[occurrence / "material.json"])
        duplicate = dict(material["pair_rows"]["groups"][0], code="alias")
        material["pair_rows"]["groups"].append(duplicate)
        data[occurrence / "material.json"] = encoded(material)
        with self.assertRaisesRegex(ValueError, "duplicate source pair"):
            self.build_fixture(data)

    def test_reference_tokens_do_not_admit_substrings_or_repaired_suffixes(self):
        occurrence, _ = fixture()
        port = "h005.f003.p.ret_response.0"
        for token in ("x" + port + "#o1", port + "_other", port + "-other",
                      port + "#_missing", port + "#o1#missing",
                      "\u00e9" + port + "#o1", port + "#o1\u00e9",
                      port + "#o1/missing", port + "#o1:missing"):
            with self.subTest(token=token):
                data = self.record_fixture()
                target = occurrence / "responses/daily/mini_prose/cycle01/objection.txt"
                # A shorter real id must not rescue a backtracked malformed token.
                data[target] = encoded({"records": [{"id": "o"}, {"id": "o1"}]})
                later = occurrence / "responses/daily/mini_prose/cycle01/ret_response.txt"
                data[later] = encoded({"mentions": [token]})
                for node, source in (("objection", target), ("ret_response", later)):
                    path = occurrence / "artifacts/daily/mini_prose/cycle01" / (node + ".json")
                    artifact = json.loads(data[path])
                    artifact["public_text_sha256"] = sha(data[source])
                    data[path] = encoded(artifact)
                path = occurrence / "traces/daily/mini_prose/cycle01/ret_response.json"
                trace = json.loads(data[path])
                trace["projection_artifacts"][1]["selected_source"]["public_text_sha256"] = sha(data[target])
                data[path] = encoded(trace)
                row = self.build_fixture(data)[0]
                self.assertEqual(row["admission"], "UNRESOLVED")
                self.assertEqual(row["referring_passages"], [])
                if token.startswith(port):
                    self.assertEqual([r["reference"]["text"] for r in row["unresolved_references"]], [token])

    def test_projection_alias_requires_an_exact_bounded_identifier(self):
        projection = "0123456789abcdef" + "a" * 48
        for token, expected in ((projection[:16], "ADMITTED"), (projection, "ADMITTED"),
                                (projection[:16] + "f" * 48, "UNRESOLVED"),
                                ("z" + projection[:16] + "z", "UNRESOLVED")):
            with self.subTest(token=token):
                occurrence, data = fixture()
                path = occurrence / "responses/daily/mini_prose/cycle01/ret_response.txt"
                data[path] = encoded({"mentions": [token]})
                artifact_path = occurrence / "artifacts/daily/mini_prose/cycle01/ret_response.json"
                artifact = json.loads(data[artifact_path])
                artifact["public_text_sha256"] = sha(data[path])
                data[artifact_path] = encoded(artifact)
                trace_path = occurrence / "traces/daily/mini_prose/cycle01/ret_response.json"
                trace = json.loads(data[trace_path])
                trace["projection_artifacts"][1]["artifact_id"] = projection
                data[trace_path] = encoded(trace)
                row = self.build_fixture(data)[0]
                self.assertEqual(row["admission"], expected)
                if expected == "ADMITTED":
                    self.assertEqual(row["referring_passages"][0]["reference"]["text"], token)

    def test_matched_native_trace_and_brief_custody(self):
        occurrence, data = fixture()
        row = self.build_fixture(data)[15]
        self.assertEqual(row["admission"], "ADMITTED")
        path = occurrence / "traces/daily/matched/cycle01/ret_response.json"
        trace = json.loads(data[path])
        self.assertEqual(trace["projection_artifacts"], [])
        trace["original_brief"] += " changed"
        data[path] = encoded(trace)
        self.assertIn("brief custody mismatch", self.build_fixture(data)[15]["reason"])
        trace["original_brief_sha256"] = sha(trace["original_brief"].encode("utf-8"))
        trace["visible_sources"].append(trace["visible_sources"][1])
        data[path] = encoded(trace)
        self.assertIn("not uniquely mapped", self.build_fixture(data)[15]["reason"])

    def test_partial_selected_view_cannot_admit_a_whole_contribution(self):
        occurrence, data = fixture()
        for arm, index in (("mini_prose", 0), ("matched", 15)):
            path = occurrence / "traces/daily" / arm / "cycle01/ret_response.json"
            trace = json.loads(data[path])
            if arm == "matched":
                trace["visible_sources"][1]["view"] = "body"
            else:
                trace["projection_artifacts"][1]["selected_source"]["view"] = "body"
            data[path] = encoded(trace)
            self.assertIn("does not expose both", self.build_fixture(data)[index]["reason"])

    def test_existing_surface_pack_accepts_new_raw_sides(self):
        from minireason.loop import packs
        row = self.build_fixture()[0]
        surface = pairs.build_surface(row)
        # The existing pack accepts Surface, preserving all its exact material.
        from minireason.loop.standard import STANDARD_BODY
        pack = packs.render_row(surface, STANDARD_BODY)
        self.assertEqual(pack.material, surface.decoded)
        self.assertEqual(pack.material_digest, surface.digest)


if __name__ == "__main__":
    unittest.main()
