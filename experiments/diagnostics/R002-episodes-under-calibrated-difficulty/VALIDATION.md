# R002 offline validation

**DRAFT; STAGED AND NOT RUN.** These are local deterministic verification and launcher fixtures, not calibration or main scientific observations. Study provider calls: zero. No .env read, source edit, docs write, git mutation or publication was performed by this task.

Final pool: 24 candidates, 18 computable, six derivation-only, 14 long-chain. Each oracle compares actual sealed answer JSON and executes its declared calculation/certificate and faulty-route check. The six proof scripts supply finite certificates or instances; their accompanying human derivations remain the universal oracle. A successful executable is not a proof of semantic correctness.

The root independently recomputed nine endpoints by separate methods (C01/C04/C08/C09/C10/C11/C13/C17/C18). Proposed second methods in other oracle records are explicitly unexecuted, not evidence.

## Exact final oracle stdout

Command from the checkout, with the mandated Python/environment:

    C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 experiments/diagnostics/R002-episodes-under-calibrated-difficulty/oracle/run_all.py

Exit code: 0. Stderr: empty. The verifier checks actual answer JSON, the 24 exact IDs, oracle kinds, direct/shared hashes, support path/hash key sets, relation IDs, reverse-given recodings and carrier payload identity. The following is the complete stdout, also retained in work/w18/oracle-final-stdout.txt and as formatted JSON in oracle/run_all.output.json.

```json
{"candidate_count":24,"carrier_checks":[{"candidate_id":"C01","payload_identity_after_tag":true},{"candidate_id":"C02","payload_identity_after_tag":true},{"candidate_id":"C03","payload_identity_after_tag":true},{"candidate_id":"C04","payload_identity_after_tag":true},{"candidate_id":"C05","payload_identity_after_tag":true},{"candidate_id":"C06","payload_identity_after_tag":true},{"candidate_id":"C07","payload_identity_after_tag":true},{"candidate_id":"C08","payload_identity_after_tag":true},{"candidate_id":"C09","payload_identity_after_tag":true},{"candidate_id":"C10","payload_identity_after_tag":true},{"candidate_id":"C11","payload_identity_after_tag":true},{"candidate_id":"C12","payload_identity_after_tag":true},{"candidate_id":"C13","payload_identity_after_tag":true},{"candidate_id":"C14","payload_identity_after_tag":true},{"candidate_id":"C15","payload_identity_after_tag":true},{"candidate_id":"C16","payload_identity_after_tag":true},{"candidate_id":"C17","payload_identity_after_tag":true},{"candidate_id":"C18","payload_identity_after_tag":true},{"candidate_id":"C19","payload_identity_after_tag":true},{"candidate_id":"C20","payload_identity_after_tag":true},{"candidate_id":"C21","payload_identity_after_tag":true},{"candidate_id":"C22","payload_identity_after_tag":true},{"candidate_id":"C23","payload_identity_after_tag":true},{"candidate_id":"C24","payload_identity_after_tag":true}],"computable_count":18,"derivation_only_count":6,"long_chain_count":14,"recoding_checks":[{"bullet_reverse":true,"candidate_id":"C01","question_identity":true,"relation_ids":["C01.posterior_C","C01.next_red"]},{"bullet_reverse":true,"candidate_id":"C02","question_identity":true,"relation_ids":["C02.bracelets","C02.rotation_classes"]},{"bullet_reverse":true,"candidate_id":"C03","question_identity":true,"relation_ids":["C03.final","C03.H"]},{"bullet_reverse":true,"candidate_id":"C04","question_identity":true,"relation_ids":["C04.rows"]},{"bullet_reverse":true,"candidate_id":"C05","question_identity":true,"relation_ids":["C05.sequence","C05.timeline","C05.objective","C05.second_objective"]},{"bullet_reverse":true,"candidate_id":"C06","question_identity":true,"relation_ids":["C06.count","C06.first"]},{"bullet_reverse":true,"candidate_id":"C07","question_identity":true,"relation_ids":["C07.expected_steps","C07.absorbed_by_5"]},{"bullet_reverse":true,"candidate_id":"C08","question_identity":true,"relation_ids":["C08.spanning_trees","C08.containing_01"]},{"bullet_reverse":true,"candidate_id":"C09","question_identity":true,"relation_ids":["C09.probability","C09.matching_strings"]},{"bullet_reverse":true,"candidate_id":"C10","question_identity":true,"relation_ids":["C10.count","C10.least","C10.sum_mod_2520"]},{"bullet_reverse":true,"candidate_id":"C11","question_identity":true,"relation_ids":["C11.sequence","C11.minimum","C11.second_distinct"]},{"bullet_reverse":true,"candidate_id":"C12","question_identity":true,"relation_ids":["C12.most_probable_state","C12.state_probability","C12.sixth_red"]},{"bullet_reverse":true,"candidate_id":"C13","question_identity":true,"relation_ids":["C13.count"]},{"bullet_reverse":true,"candidate_id":"C14","question_identity":true,"relation_ids":["C14.x_20","C14.H"]},{"bullet_reverse":true,"candidate_id":"C15","question_identity":true,"relation_ids":["C15.arrival","C15.route"]},{"bullet_reverse":true,"candidate_id":"C16","question_identity":true,"relation_ids":["C16.winning","C16.remoteness","C16.optimal_first_moves"]},{"bullet_reverse":true,"candidate_id":"C17","question_identity":true,"relation_ids":["C17.P20","C17.coefficient_x7"]},{"bullet_reverse":true,"candidate_id":"C18","question_identity":true,"relation_ids":["C18.completions","C18.turnaround_sum"]},{"bullet_reverse":true,"candidate_id":"C19","question_identity":true,"relation_ids":["C19.identity","C19.domain"]},{"bullet_reverse":true,"candidate_id":"C20","question_identity":true,"relation_ids":["C20.identity","C20.singular_included"]},{"bullet_reverse":true,"candidate_id":"C21","question_identity":true,"relation_ids":["C21.closed_form","C21.at_x_1"]},{"bullet_reverse":true,"candidate_id":"C22","question_identity":true,"relation_ids":["C22.P(x)"]},{"bullet_reverse":true,"candidate_id":"C23","question_identity":true,"relation_ids":["C23.identity"]},{"bullet_reverse":true,"candidate_id":"C24","question_identity":true,"relation_ids":["C24.inverse","C24.A17"]}],"results":[{"candidate_id":"C01","oracle_kind":"computable","output_path":"oracle/C01.output.json","output_sha256":"1197322c55f7d31f9aeb711d24d2eaf8738bb6df631c0adac0b6a43354d6c0bc"},{"candidate_id":"C02","oracle_kind":"computable","output_path":"oracle/C02.output.json","output_sha256":"e985c2f5d446731d86afd128de1f3d284860077ceb98030ee8d1294166fbf712"},{"candidate_id":"C03","oracle_kind":"computable","output_path":"oracle/C03.output.json","output_sha256":"f5b81b7adb324d4552d83df3fd618450762aed03348931dedc1163d7103ba424"},{"candidate_id":"C04","oracle_kind":"computable","output_path":"oracle/C04.output.json","output_sha256":"e0aa3c94beffc7b46007be7df6603153e97bd69cfa226b180def611f77b256f4"},{"candidate_id":"C05","oracle_kind":"computable","output_path":"oracle/C05.output.json","output_sha256":"2c1f7b0cf0bd318af78385332f5df86b2129f2b6b403e5deb4eac73ccfe57601"},{"candidate_id":"C06","oracle_kind":"computable","output_path":"oracle/C06.output.json","output_sha256":"cfbdeaebcaec74407a0afd2c82d1509ed667706364ddfb82a2fcb598a34d594f"},{"candidate_id":"C07","oracle_kind":"computable","output_path":"oracle/C07.output.json","output_sha256":"feae881e6f850d3235f7311692c6da168953677e027901655a4284a8511bab08"},{"candidate_id":"C08","oracle_kind":"computable","output_path":"oracle/C08.output.json","output_sha256":"354f234937ba59206ad06c581ddd72a354c73e805a511674cdf14d06884b9eef"},{"candidate_id":"C09","oracle_kind":"computable","output_path":"oracle/C09.output.json","output_sha256":"2f035dc9a83345b9a7b8eebb9e524a18ba2754f0ef0e79dafff708b4ad7d644f"},{"candidate_id":"C10","oracle_kind":"computable","output_path":"oracle/C10.output.json","output_sha256":"861c8219543a1e2d66ff2b0139ede2f57d85bf0545df9dee6982f6d7d44f3958"},{"candidate_id":"C11","oracle_kind":"computable","output_path":"oracle/C11.output.json","output_sha256":"a4fff7826882a99ea6a5e4ecbef7f7c9aa0a1ba34d3d8852dd7097f78c012749"},{"candidate_id":"C12","oracle_kind":"computable","output_path":"oracle/C12.output.json","output_sha256":"b50eaa1c4f5b238f8f20a9c6644f586a752dd8a6c6beb5c4b047dcba22b98e18"},{"candidate_id":"C13","oracle_kind":"computable","output_path":"oracle/C13.output.json","output_sha256":"7b38494218047749c8d997fedba1c106cd6d6305c19b8be18ad0bb755519a9f5"},{"candidate_id":"C14","oracle_kind":"computable","output_path":"oracle/C14.output.json","output_sha256":"2b39d757ee779d7e7ec2acb6d066b287ce2b926c3a8802b460a096cabd28ba11"},{"candidate_id":"C15","oracle_kind":"computable","output_path":"oracle/C15.output.json","output_sha256":"801c9976da0181a539330917c53087a1295b425d3f49dd3885f7167c26bcaf53"},{"candidate_id":"C16","oracle_kind":"computable","output_path":"oracle/C16.output.json","output_sha256":"6a0572e0f3536c2f7aeca8373e45be6e41919ce47d3175663976d38a8ced8cd0"},{"candidate_id":"C17","oracle_kind":"computable","output_path":"oracle/C17.output.json","output_sha256":"8b46b503debaff65aecf3f366907a3ab1a85ba91c39c2b15cf6d4580b1f27222"},{"candidate_id":"C18","oracle_kind":"computable","output_path":"oracle/C18.output.json","output_sha256":"7719e031d9e69d5b92a74a72d7c5266fecdba4b824155a21dbe6f8c690f3afd1"},{"candidate_id":"C19","oracle_kind":"derivation-only","output_path":"oracle/C19.output.json","output_sha256":"33dd50a0e58b10f5e89987c292b05707e3ab61cfd0e2abd4869db18426109137"},{"candidate_id":"C20","oracle_kind":"derivation-only","output_path":"oracle/C20.output.json","output_sha256":"8f328cf7017153c3134bb353fdafb458c29a2cf93a5b3fcf5661f5675cbe1e67"},{"candidate_id":"C21","oracle_kind":"derivation-only","output_path":"oracle/C21.output.json","output_sha256":"8bb7bc88d75a2eb684c0d98c93fc6fa1218a2ad2d1592633bd3d7f8286cdd7ea"},{"candidate_id":"C22","oracle_kind":"derivation-only","output_path":"oracle/C22.output.json","output_sha256":"a5efd9b68060cdcd4d2daeac77bec188edd934579c561dfbb2da5c31129eb0bd"},{"candidate_id":"C23","oracle_kind":"derivation-only","output_path":"oracle/C23.output.json","output_sha256":"e9ac78b63051b1cfb51c1271280c687137c4586b15754ac48a87c70c3e59a9c7"},{"candidate_id":"C24","oracle_kind":"derivation-only","output_path":"oracle/C24.output.json","output_sha256":"628b971d6e980e4cabc9ffd2f6fdb500ef62b341d7a0b56508e52d912b650ad6"}],"status":"PASS"}
```

## Exact final launcher transcript

Occurrence002 preserves occurrence001. The transcript includes exact commands and output for unit tests, oracle checks, calibration and main fixtures, and the actual existing CLI offline CROSS run. The first transcript wrapper failed after child completion on a nonexistent config field; its corrected reader recovered saved occurrence002 evidence without rerunning either phase. All seven unit tests passed; both phases exited 0; all eight computable-case conditions were scheduled. Legacy CROSS executed 13 offline logical slots with conditional closing absent and stopped at cycle_budget. New-arm fixtures only describe the intended 14 slots and do not implement or qualify those seats. Longest legacy absolute path: 102 characters.

```text
UNIT COMMAND
C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 -m unittest C:\Dev\miniReason\experiments\diagnostics\R002-episodes-under-calibrated-difficulty\tests\test_run_R002.py -v
UNIT RETURN 0
STDOUT

STDERR
test_admission_is_first_eight_incorrect_or_no_answer_in_id_order (experiments.diagnostics.R002-episodes-under-calibrated-difficulty.tests.test_run_R002.R002LauncherTests.test_admission_is_first_eight_incorrect_or_no_answer_in_id_order) ... ok
test_fewer_than_eight_and_zero_follow_stopping_rule (experiments.diagnostics.R002-episodes-under-calibrated-difficulty.tests.test_run_R002.R002LauncherTests.test_fewer_than_eight_and_zero_follow_stopping_rule) ... ok
test_live_is_blocked_without_engineering_adapter (experiments.diagnostics.R002-episodes-under-calibrated-difficulty.tests.test_run_R002.R002LauncherTests.test_live_is_blocked_without_engineering_adapter) ... ok
test_live_receipt_links_all_24_trials_and_sealed_hashes (experiments.diagnostics.R002-episodes-under-calibrated-difficulty.tests.test_run_R002.R002LauncherTests.test_live_receipt_links_all_24_trials_and_sealed_hashes) ... ok
test_maximum_budget_matches_preregistration (experiments.diagnostics.R002-episodes-under-calibrated-difficulty.tests.test_run_R002.R002LauncherTests.test_maximum_budget_matches_preregistration) ... ok
test_proposed_contract_artifacts_are_pinned (experiments.diagnostics.R002-episodes-under-calibrated-difficulty.tests.test_run_R002.R002LauncherTests.test_proposed_contract_artifacts_are_pinned) ... ok
test_write_once_receipt_refuses_overwrite (experiments.diagnostics.R002-episodes-under-calibrated-difficulty.tests.test_run_R002.R002LauncherTests.test_write_once_receipt_refuses_overwrite) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.196s

OK


ORACLE COMMAND
C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 C:\Dev\miniReason\experiments\diagnostics\R002-episodes-under-calibrated-difficulty\oracle\run_all.py
ORACLE RETURN 0
STDOUT
{"candidate_count":24,"carrier_checks":[{"candidate_id":"C01","payload_identity_after_tag":true},{"candidate_id":"C02","payload_identity_after_tag":true},{"candidate_id":"C03","payload_identity_after_tag":true},{"candidate_id":"C04","payload_identity_after_tag":true},{"candidate_id":"C05","payload_identity_after_tag":true},{"candidate_id":"C06","payload_identity_after_tag":true},{"candidate_id":"C07","payload_identity_after_tag":true},{"candidate_id":"C08","payload_identity_after_tag":true},{"candidate_id":"C09","payload_identity_after_tag":true},{"candidate_id":"C10","payload_identity_after_tag":true},{"candidate_id":"C11","payload_identity_after_tag":true},{"candidate_id":"C12","payload_identity_after_tag":true},{"candidate_id":"C13","payload_identity_after_tag":true},{"candidate_id":"C14","payload_identity_after_tag":true},{"candidate_id":"C15","payload_identity_after_tag":true},{"candidate_id":"C16","payload_identity_after_tag":true},{"candidate_id":"C17","payload_identity_after_tag":true},{"candidate_id":"C18","payload_identity_after_tag":true},{"candidate_id":"C19","payload_identity_after_tag":true},{"candidate_id":"C20","payload_identity_after_tag":true},{"candidate_id":"C21","payload_identity_after_tag":true},{"candidate_id":"C22","payload_identity_after_tag":true},{"candidate_id":"C23","payload_identity_after_tag":true},{"candidate_id":"C24","payload_identity_after_tag":true}],"computable_count":18,"derivation_only_count":6,"long_chain_count":14,"recoding_checks":[{"bullet_reverse":true,"candidate_id":"C01","question_identity":true,"relation_ids":["C01.posterior_C","C01.next_red"]},{"bullet_reverse":true,"candidate_id":"C02","question_identity":true,"relation_ids":["C02.bracelets","C02.rotation_classes"]},{"bullet_reverse":true,"candidate_id":"C03","question_identity":true,"relation_ids":["C03.final","C03.H"]},{"bullet_reverse":true,"candidate_id":"C04","question_identity":true,"relation_ids":["C04.rows"]},{"bullet_reverse":true,"candidate_id":"C05","question_identity":true,"relation_ids":["C05.sequence","C05.timeline","C05.objective","C05.second_objective"]},{"bullet_reverse":true,"candidate_id":"C06","question_identity":true,"relation_ids":["C06.count","C06.first"]},{"bullet_reverse":true,"candidate_id":"C07","question_identity":true,"relation_ids":["C07.expected_steps","C07.absorbed_by_5"]},{"bullet_reverse":true,"candidate_id":"C08","question_identity":true,"relation_ids":["C08.spanning_trees","C08.containing_01"]},{"bullet_reverse":true,"candidate_id":"C09","question_identity":true,"relation_ids":["C09.probability","C09.matching_strings"]},{"bullet_reverse":true,"candidate_id":"C10","question_identity":true,"relation_ids":["C10.count","C10.least","C10.sum_mod_2520"]},{"bullet_reverse":true,"candidate_id":"C11","question_identity":true,"relation_ids":["C11.sequence","C11.minimum","C11.second_distinct"]},{"bullet_reverse":true,"candidate_id":"C12","question_identity":true,"relation_ids":["C12.most_probable_state","C12.state_probability","C12.sixth_red"]},{"bullet_reverse":true,"candidate_id":"C13","question_identity":true,"relation_ids":["C13.count"]},{"bullet_reverse":true,"candidate_id":"C14","question_identity":true,"relation_ids":["C14.x_20","C14.H"]},{"bullet_reverse":true,"candidate_id":"C15","question_identity":true,"relation_ids":["C15.arrival","C15.route"]},{"bullet_reverse":true,"candidate_id":"C16","question_identity":true,"relation_ids":["C16.winning","C16.remoteness","C16.optimal_first_moves"]},{"bullet_reverse":true,"candidate_id":"C17","question_identity":true,"relation_ids":["C17.P20","C17.coefficient_x7"]},{"bullet_reverse":true,"candidate_id":"C18","question_identity":true,"relation_ids":["C18.completions","C18.turnaround_sum"]},{"bullet_reverse":true,"candidate_id":"C19","question_identity":true,"relation_ids":["C19.identity","C19.domain"]},{"bullet_reverse":true,"candidate_id":"C20","question_identity":true,"relation_ids":["C20.identity","C20.singular_included"]},{"bullet_reverse":true,"candidate_id":"C21","question_identity":true,"relation_ids":["C21.closed_form","C21.at_x_1"]},{"bullet_reverse":true,"candidate_id":"C22","question_identity":true,"relation_ids":["C22.P(x)"]},{"bullet_reverse":true,"candidate_id":"C23","question_identity":true,"relation_ids":["C23.identity"]},{"bullet_reverse":true,"candidate_id":"C24","question_identity":true,"relation_ids":["C24.inverse","C24.A17"]}],"results":[{"candidate_id":"C01","oracle_kind":"computable","output_path":"oracle/C01.output.json","output_sha256":"1197322c55f7d31f9aeb711d24d2eaf8738bb6df631c0adac0b6a43354d6c0bc"},{"candidate_id":"C02","oracle_kind":"computable","output_path":"oracle/C02.output.json","output_sha256":"e985c2f5d446731d86afd128de1f3d284860077ceb98030ee8d1294166fbf712"},{"candidate_id":"C03","oracle_kind":"computable","output_path":"oracle/C03.output.json","output_sha256":"f5b81b7adb324d4552d83df3fd618450762aed03348931dedc1163d7103ba424"},{"candidate_id":"C04","oracle_kind":"computable","output_path":"oracle/C04.output.json","output_sha256":"e0aa3c94beffc7b46007be7df6603153e97bd69cfa226b180def611f77b256f4"},{"candidate_id":"C05","oracle_kind":"computable","output_path":"oracle/C05.output.json","output_sha256":"2c1f7b0cf0bd318af78385332f5df86b2129f2b6b403e5deb4eac73ccfe57601"},{"candidate_id":"C06","oracle_kind":"computable","output_path":"oracle/C06.output.json","output_sha256":"cfbdeaebcaec74407a0afd2c82d1509ed667706364ddfb82a2fcb598a34d594f"},{"candidate_id":"C07","oracle_kind":"computable","output_path":"oracle/C07.output.json","output_sha256":"feae881e6f850d3235f7311692c6da168953677e027901655a4284a8511bab08"},{"candidate_id":"C08","oracle_kind":"computable","output_path":"oracle/C08.output.json","output_sha256":"354f234937ba59206ad06c581ddd72a354c73e805a511674cdf14d06884b9eef"},{"candidate_id":"C09","oracle_kind":"computable","output_path":"oracle/C09.output.json","output_sha256":"2f035dc9a83345b9a7b8eebb9e524a18ba2754f0ef0e79dafff708b4ad7d644f"},{"candidate_id":"C10","oracle_kind":"computable","output_path":"oracle/C10.output.json","output_sha256":"861c8219543a1e2d66ff2b0139ede2f57d85bf0545df9dee6982f6d7d44f3958"},{"candidate_id":"C11","oracle_kind":"computable","output_path":"oracle/C11.output.json","output_sha256":"a4fff7826882a99ea6a5e4ecbef7f7c9aa0a1ba34d3d8852dd7097f78c012749"},{"candidate_id":"C12","oracle_kind":"computable","output_path":"oracle/C12.output.json","output_sha256":"b50eaa1c4f5b238f8f20a9c6644f586a752dd8a6c6beb5c4b047dcba22b98e18"},{"candidate_id":"C13","oracle_kind":"computable","output_path":"oracle/C13.output.json","output_sha256":"7b38494218047749c8d997fedba1c106cd6d6305c19b8be18ad0bb755519a9f5"},{"candidate_id":"C14","oracle_kind":"computable","output_path":"oracle/C14.output.json","output_sha256":"2b39d757ee779d7e7ec2acb6d066b287ce2b926c3a8802b460a096cabd28ba11"},{"candidate_id":"C15","oracle_kind":"computable","output_path":"oracle/C15.output.json","output_sha256":"801c9976da0181a539330917c53087a1295b425d3f49dd3885f7167c26bcaf53"},{"candidate_id":"C16","oracle_kind":"computable","output_path":"oracle/C16.output.json","output_sha256":"6a0572e0f3536c2f7aeca8373e45be6e41919ce47d3175663976d38a8ced8cd0"},{"candidate_id":"C17","oracle_kind":"computable","output_path":"oracle/C17.output.json","output_sha256":"8b46b503debaff65aecf3f366907a3ab1a85ba91c39c2b15cf6d4580b1f27222"},{"candidate_id":"C18","oracle_kind":"computable","output_path":"oracle/C18.output.json","output_sha256":"7719e031d9e69d5b92a74a72d7c5266fecdba4b824155a21dbe6f8c690f3afd1"},{"candidate_id":"C19","oracle_kind":"derivation-only","output_path":"oracle/C19.output.json","output_sha256":"33dd50a0e58b10f5e89987c292b05707e3ab61cfd0e2abd4869db18426109137"},{"candidate_id":"C20","oracle_kind":"derivation-only","output_path":"oracle/C20.output.json","output_sha256":"8f328cf7017153c3134bb353fdafb458c29a2cf93a5b3fcf5661f5675cbe1e67"},{"candidate_id":"C21","oracle_kind":"derivation-only","output_path":"oracle/C21.output.json","output_sha256":"8bb7bc88d75a2eb684c0d98c93fc6fa1218a2ad2d1592633bd3d7f8286cdd7ea"},{"candidate_id":"C22","oracle_kind":"derivation-only","output_path":"oracle/C22.output.json","output_sha256":"a5efd9b68060cdcd4d2daeac77bec188edd934579c561dfbb2da5c31129eb0bd"},{"candidate_id":"C23","oracle_kind":"derivation-only","output_path":"oracle/C23.output.json","output_sha256":"e9ac78b63051b1cfb51c1271280c687137c4586b15754ac48a87c70c3e59a9c7"},{"candidate_id":"C24","oracle_kind":"derivation-only","output_path":"oracle/C24.output.json","output_sha256":"628b971d6e980e4cabc9ffd2f6fdb500ef62b341d7a0b56508e52d912b650ad6"}],"status":"PASS"}

STDERR


CURRENT SCHEMA_RECIPE PINS
{"recipes": [["r002-carrier-v1.json", "e189ab7d961677df4dced1f29894c586c73d6696196968e0fa0e2b932357916a", "r002-carrier-v1", 14, 14], ["r002-checker-v1.json", "e629fd024a4ddd950ecab947696a9dbeac653ef5c35635ae5023c315a5f932a2", "r002-checker-v1", 14, 14], ["r002-cross-match-v1.json", "32e69459cbcdd40ab1ea01e451257a8e09be6c4a24ce2ae167007d163832f0b5", "r002-cross-match-v1", 14, 14], ["r002-native-match-v1.json", "9b51f5c7f28c5b37ff7f20ec221d02c1e42878c23ba9e7e770d0d46c18c23ac8", "r002-native-match-v1", 14, 14], ["r002-recoded-v1.json", "0e6b05b72c34af2a8b01fd58a6e8324d5de325b72292455a9fa17e59d5ce56a0", "r002-recoded-v1", 14, 14], ["r002-tested-cross-v1.json", "dd0a4975a9d41879998e9f969faca4fabe236c409be652570c939393dfc712f3", "r002-tested-cross-v1", 14, 14]], "recipes_checked": 6, "schema_hashes": {"answer.schema.json": "c5b54d66584bbc8c25a698257171b6e0e222898615201c631ef6221d95e7cbf6", "checker-execution.schema.json": "5be7f778a5b6fd5f7f0990c696b3885cc9e1b35bae5061b5aec3c2c661b698a2", "checker-proposal.schema.json": "28ef41d4be24a3faa93c6fc8a6fa7d4e0f641050f47c49b6c485840525e3d4ad", "coding-manifest.schema.json": "f6a2deab8fa40b60a865d1911f3abb6a7d821aa1d6b55df5e5e09172f7d5e74c", "native-match-note.schema.json": "78a6b008fec97c79455811c126ad8ba9fea206327ed3cc65a5dc4d4593077a25", "propagation-use.schema.json": "12dbef8f3ce52efc2819fe1c8be3335cd77f20156e860c504a44e1e51745fdd4", "prose-objection.schema.json": "e81a1677a6b88617cbcfc24f0f3bef8857e80a2439375c2ba72986ee742a5839", "prose-return.schema.json": "d4c5348d81673cbb9f9f6cdb423f31fc2bef38022649364a85be873b5a07b538", "recoding-solve.schema.json": "d5e867b8a25931eebfa7708f21eb49f9f91d63927e1ea712b5d93c249d6d0350", "relations.schema.json": "e005b3b510b2a7027c89a166cdc2789388c4a54a9c6aa1d6da66f8c2dab88f13", "tested-objection.schema.json": "a3b092330c5bb807f3da54e4c069e4f370461a65db369bb3372895de4eae865f", "tested-return.schema.json": "302414bcb96037e3cb20535a9f3b51de6c756bb5e6ef822845beda7f7b7dcdce"}, "schemas_checked": 12}

CURRENT CANDIDATE PINS
{"c01_hashes": {"answer_sha256": "fc2230a7e8e739ae773b05f2324514796dc967e4a579bd71e2f2d54618ef4e23", "carrier_problem_sha256": "cd56cf694a4cfa75086bd1c91378618ca1f48be72a80a314e3988ab80ba28d65", "oracle_sha256": "94237b7ea403c1c4d10d3bf71fc031f563110fc336e6f64f011fe543aa87cbe3", "problem_sha256": "6edf0407907062513b00d0408fc6517ffabc7b9d8ed3b08b91fa99478b7cd000", "recoded_problem_sha256": "ddb6c1d451f2729d72fc141ec1716ae3e10932924fbd989792a746172e8e370a"}, "manifest_sha256": "b124fbdd9db1af4d99eb411774804f17604982308c277484e8a82247946a52ee", "oracle_support_sha256": {"oracle/_calculations.py": "ac7db5ca3bd65c790d6e7925a3a79dd093d2726774c52751647886d36c6a57fe"}}

CALIBRATION COMMAND
C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 C:\Dev\miniReason\experiments\diagnostics\R002-episodes-under-calibrated-difficulty\run_R002.py --phase calibration --mode offline --occurrence 2 --run-root work/w18/o --problems C01
CALIBRATION RETURN 0
OUTPUT
Original child output was not retained because the first transcript wrapper failed after both child runs completed. The immutable terminal receipt is reproduced below. The child is not rerun.

MAIN COMMAND
C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 C:\Dev\miniReason\experiments\diagnostics\R002-episodes-under-calibrated-difficulty\run_R002.py --phase main --mode offline --occurrence 2 --run-root work/w18/o --admission-receipt work/w18/o-admission-002.json --problems C01
MAIN RETURN 0
OUTPUT
Original child output was not retained because the first transcript wrapper failed after both child runs completed. The immutable terminal receipt and legacy stdout/stderr hashes are reproduced below. The child is not rerun.

CALIBRATION RECEIPT
{
  "admission_eligible": false,
  "candidate_manifest_path": "CANDIDATES.md",
  "candidate_manifest_sha256": "7f1e20ae2172ea2e90def0c5d102a74cb0df6e3ce8d314e4ba278b9348f5e887",
  "created_utc": "2026-09-16T20:51:47.959190+00:00",
  "export_allowlist": [
    "calibration-occurrence-002/C01/CAL-NATIVE/fixture.json",
    "calibration-occurrence-002/phase-receipt.json"
  ],
  "mode": "offline",
  "occurrence": 2,
  "phase": "calibration",
  "pilot_output_allowed_in_main_prompts": false,
  "proposed_artifact_sha256": {
    "contracts": {
      "contracts/answer.schema.json": "c5b54d66584bbc8c25a698257171b6e0e222898615201c631ef6221d95e7cbf6",
      "contracts/checker-execution.schema.json": "5be7f778a5b6fd5f7f0990c696b3885cc9e1b35bae5061b5aec3c2c661b698a2",
      "contracts/checker-proposal.schema.json": "28ef41d4be24a3faa93c6fc8a6fa7d4e0f641050f47c49b6c485840525e3d4ad",
      "contracts/coding-manifest.schema.json": "f6a2deab8fa40b60a865d1911f3abb6a7d821aa1d6b55df5e5e09172f7d5e74c",
      "contracts/native-match-note.schema.json": "78a6b008fec97c79455811c126ad8ba9fea206327ed3cc65a5dc4d4593077a25",
      "contracts/propagation-use.schema.json": "12dbef8f3ce52efc2819fe1c8be3335cd77f20156e860c504a44e1e51745fdd4",
      "contracts/prose-objection.schema.json": "e81a1677a6b88617cbcfc24f0f3bef8857e80a2439375c2ba72986ee742a5839",
      "contracts/prose-return.schema.json": "d4c5348d81673cbb9f9f6cdb423f31fc2bef38022649364a85be873b5a07b538",
      "contracts/recoding-solve.schema.json": "d5e867b8a25931eebfa7708f21eb49f9f91d63927e1ea712b5d93c249d6d0350",
      "contracts/relations.schema.json": "e005b3b510b2a7027c89a166cdc2789388c4a54a9c6aa1d6da66f8c2dab88f13",
      "contracts/tested-objection.schema.json": "a3b092330c5bb807f3da54e4c069e4f370461a65db369bb3372895de4eae865f",
      "contracts/tested-return.schema.json": "302414bcb96037e3cb20535a9f3b51de6c756bb5e6ef822845beda7f7b7dcdce"
    },
    "recipes": {
      "recipes/r002-carrier-v1.json": "e189ab7d961677df4dced1f29894c586c73d6696196968e0fa0e2b932357916a",
      "recipes/r002-checker-v1.json": "e629fd024a4ddd950ecab947696a9dbeac653ef5c35635ae5023c315a5f932a2",
      "recipes/r002-cross-match-v1.json": "32e69459cbcdd40ab1ea01e451257a8e09be6c4a24ce2ae167007d163832f0b5",
      "recipes/r002-native-match-v1.json": "9b51f5c7f28c5b37ff7f20ec221d02c1e42878c23ba9e7e770d0d46c18c23ac8",
      "recipes/r002-recoded-v1.json": "0e6b05b72c34af2a8b01fd58a6e8324d5de325b72292455a9fa17e59d5ce56a0",
      "recipes/r002-tested-cross-v1.json": "dd0a4975a9d41879998e9f969faca4fabe236c409be652570c939393dfc712f3"
    }
  },
  "records": [
    {
      "baseline_run_id": null,
      "candidate_id": "C01",
      "fixture_path": "calibration-occurrence-002/C01/CAL-NATIVE/fixture.json",
      "occurrence_id": "R002-C01-CAL-NATIVE-attempt-002",
      "oracle_kind": "computable",
      "oracle_sha256": "94237b7ea403c1c4d10d3bf71fc031f563110fc336e6f64f011fe543aa87cbe3",
      "problem_sha256": "6edf0407907062513b00d0408fc6517ffabc7b9d8ed3b08b91fa99478b7cd000",
      "sealed_answer_sha256": "fc2230a7e8e739ae773b05f2324514796dc967e4a579bd71e2f2d54618ef4e23"
    }
  ],
  "schema": "minireason.r002.launcher.v1",
  "scientific_evidence": false,
  "selected_candidates": [
    "C01"
  ]
}


MAIN RECEIPT
{
  "admission_evidence_kind": "offline-test-fixture",
  "admission_receipt_path": "C:\\Dev\\miniReason\\work\\w18\\o-admission-002.json",
  "admission_receipt_sha256": "6800538c5da76e5fd1aeeb02654889dcceb3e9e61cc28fbe74376a09dcfe0815",
  "admitted": [
    "C01"
  ],
  "budget": {
    "admitted": 1,
    "calibration_candidates": 24,
    "combined_token_ceiling": 7536640,
    "completion_token_ceiling": 2883584,
    "computable_admitted": 1,
    "logical_calls": 123,
    "maximum_attempts": 142,
    "per_attempt_wall_seconds": 300,
    "prompt_token_ceiling": 4653056
  },
  "created_utc": "2026-09-16T20:51:48.866085+00:00",
  "credential_name_allowlist": [
    "DEEPSEEK_API_KEY",
    "OLLAMA_API_KEY"
  ],
  "export_allowlist": [
    "main-occurrence-002/C01/NATIVE/fixture.json",
    "main-occurrence-002/C01/LOOP-CROSS/launcher-receipt.json",
    "main-occurrence-002/C01/LOOP-CROSS-MATCH/fixture.json",
    "main-occurrence-002/C01/LOOP-TESTED/fixture.json",
    "main-occurrence-002/C01/LOOP-RECODED/fixture.json",
    "main-occurrence-002/C01/LOOP-CARRIER/fixture.json",
    "main-occurrence-002/C01/NATIVE-MATCH/fixture.json",
    "main-occurrence-002/C01/LOOP-CHECKER/fixture.json",
    "main-occurrence-002/phase-receipt.json"
  ],
  "main_input_allowlist": [
    "problems/C01.txt",
    "problems/carrier/C01.txt",
    "problems/recoded/C01.txt"
  ],
  "mode": "offline",
  "occurrence": 2,
  "phase": "main",
  "pilot_output_allowed_in_main_prompts": false,
  "proposed_artifact_sha256": {
    "contracts": {
      "contracts/answer.schema.json": "c5b54d66584bbc8c25a698257171b6e0e222898615201c631ef6221d95e7cbf6",
      "contracts/checker-execution.schema.json": "5be7f778a5b6fd5f7f0990c696b3885cc9e1b35bae5061b5aec3c2c661b698a2",
      "contracts/checker-proposal.schema.json": "28ef41d4be24a3faa93c6fc8a6fa7d4e0f641050f47c49b6c485840525e3d4ad",
      "contracts/coding-manifest.schema.json": "f6a2deab8fa40b60a865d1911f3abb6a7d821aa1d6b55df5e5e09172f7d5e74c",
      "contracts/native-match-note.schema.json": "78a6b008fec97c79455811c126ad8ba9fea206327ed3cc65a5dc4d4593077a25",
      "contracts/propagation-use.schema.json": "12dbef8f3ce52efc2819fe1c8be3335cd77f20156e860c504a44e1e51745fdd4",
      "contracts/prose-objection.schema.json": "e81a1677a6b88617cbcfc24f0f3bef8857e80a2439375c2ba72986ee742a5839",
      "contracts/prose-return.schema.json": "d4c5348d81673cbb9f9f6cdb423f31fc2bef38022649364a85be873b5a07b538",
      "contracts/recoding-solve.schema.json": "d5e867b8a25931eebfa7708f21eb49f9f91d63927e1ea712b5d93c249d6d0350",
      "contracts/relations.schema.json": "e005b3b510b2a7027c89a166cdc2789388c4a54a9c6aa1d6da66f8c2dab88f13",
      "contracts/tested-objection.schema.json": "a3b092330c5bb807f3da54e4c069e4f370461a65db369bb3372895de4eae865f",
      "contracts/tested-return.schema.json": "302414bcb96037e3cb20535a9f3b51de6c756bb5e6ef822845beda7f7b7dcdce"
    },
    "recipes": {
      "recipes/r002-carrier-v1.json": "e189ab7d961677df4dced1f29894c586c73d6696196968e0fa0e2b932357916a",
      "recipes/r002-checker-v1.json": "e629fd024a4ddd950ecab947696a9dbeac653ef5c35635ae5023c315a5f932a2",
      "recipes/r002-cross-match-v1.json": "32e69459cbcdd40ab1ea01e451257a8e09be6c4a24ce2ae167007d163832f0b5",
      "recipes/r002-native-match-v1.json": "9b51f5c7f28c5b37ff7f20ec221d02c1e42878c23ba9e7e770d0d46c18c23ac8",
      "recipes/r002-recoded-v1.json": "0e6b05b72c34af2a8b01fd58a6e8324d5de325b72292455a9fa17e59d5ce56a0",
      "recipes/r002-tested-cross-v1.json": "dd0a4975a9d41879998e9f969faca4fabe236c409be652570c939393dfc712f3"
    }
  },
  "records": [
    {
      "candidate_id": "C01",
      "condition": "NATIVE",
      "evidence_path": "main-occurrence-002/C01/NATIVE/fixture.json",
      "status": "OFFLINE_STRUCTURAL_FIXTURE"
    },
    {
      "candidate_id": "C01",
      "condition": "LOOP-CROSS",
      "evidence_path": "main-occurrence-002/C01/LOOP-CROSS/launcher-receipt.json",
      "status": "actual-existing-cli-offline"
    },
    {
      "candidate_id": "C01",
      "condition": "LOOP-CROSS-MATCH",
      "evidence_path": "main-occurrence-002/C01/LOOP-CROSS-MATCH/fixture.json",
      "status": "OFFLINE_STRUCTURAL_FIXTURE"
    },
    {
      "candidate_id": "C01",
      "condition": "LOOP-TESTED",
      "evidence_path": "main-occurrence-002/C01/LOOP-TESTED/fixture.json",
      "status": "OFFLINE_STRUCTURAL_FIXTURE"
    },
    {
      "candidate_id": "C01",
      "condition": "LOOP-RECODED",
      "evidence_path": "main-occurrence-002/C01/LOOP-RECODED/fixture.json",
      "status": "OFFLINE_STRUCTURAL_FIXTURE"
    },
    {
      "candidate_id": "C01",
      "condition": "LOOP-CARRIER",
      "evidence_path": "main-occurrence-002/C01/LOOP-CARRIER/fixture.json",
      "status": "OFFLINE_STRUCTURAL_FIXTURE"
    },
    {
      "candidate_id": "C01",
      "condition": "NATIVE-MATCH",
      "evidence_path": "main-occurrence-002/C01/NATIVE-MATCH/fixture.json",
      "status": "OFFLINE_STRUCTURAL_FIXTURE"
    },
    {
      "candidate_id": "C01",
      "condition": "LOOP-CHECKER",
      "evidence_path": "main-occurrence-002/C01/LOOP-CHECKER/fixture.json",
      "status": "OFFLINE_STRUCTURAL_FIXTURE"
    }
  ],
  "schema": "minireason.r002.launcher.v1",
  "scientific_evidence": false,
  "stopping_rule": "first eight incorrect/no_answer in ascending candidate ID; all 1-7 if fewer; stop at zero"
}


LEGACY RECEIPT
{
  "action": "actual-existing-cli-offline",
  "candidate_id": "C01",
  "condition": "LOOP-CROSS",
  "descriptive_alias": "main-occurrence-002/C01/LOOP-CROSS",
  "note": "Actual existing CLI offline fixture; it validates legacy routing, not answer quality.",
  "returncode": 0,
  "run_directory": "C:\\Dev\\miniReason\\work\\w18\\r2o\\c506ad56cf\\c01x",
  "scientific_evidence": false,
  "stderr_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "stdout_sha256": "6a93a49f742b9548e128d252f03e10309d02acf3f81388921bf8367002c2d2ff",
  "stop_reason": "cycle_budget"
}


SCHEDULE AND PATH ASSERTIONS
{"conditions": ["NATIVE", "LOOP-CROSS", "LOOP-CROSS-MATCH", "LOOP-TESTED", "LOOP-RECODED", "LOOP-CARRIER", "NATIVE-MATCH", "LOOP-CHECKER"], "engine_files": 64, "legacy": {"action": "actual-existing-cli-offline", "logical_call_directories": ["c0001-k01", "c0001-k02", "c0001-return", "c0001-use", "c0002-k01", "c0002-k02", "c0002-return", "c0002-use", "c0003-k01", "c0003-k02", "c0003-return", "c0003-use", "initial"], "logical_calls_observed": 13, "mode": "offline", "recipe": "cross-family", "recipe_sha256": "04bf836ad436d0458f543e61adbd5c9b8b6a3cfb96606f22633857e59a0a0494", "returncode": 0, "stop_reason": "cycle_budget"}, "max_absolute_path": 102, "strict_fixtures": {"LOOP-CARRIER": {"calls_made": 0, "intended_live_calls": 14, "scientific_evidence": false}, "LOOP-CHECKER": {"calls_made": 0, "intended_live_calls": 14, "scientific_evidence": false}, "LOOP-CROSS-MATCH": {"calls_made": 0, "intended_live_calls": 14, "scientific_evidence": false}, "LOOP-RECODED": {"calls_made": 0, "intended_live_calls": 14, "scientific_evidence": false}, "LOOP-TESTED": {"calls_made": 0, "intended_live_calls": 14, "scientific_evidence": false}, "NATIVE": {"calls_made": 0, "intended_live_calls": 1, "scientific_evidence": false}, "NATIVE-MATCH": {"calls_made": 0, "intended_live_calls": 14, "scientific_evidence": false}}}

FINAL ASSERTIONS
{"calibration_return": 0, "environment_file_read": false, "main_return": 0, "occurrence_001_preserved": true, "oracle_return": 0, "provider_calls": 0, "scientific_evidence": false, "transcript_wrapper_recovery": "first wrapper failed after child completion on nonexistent config recipe_name field; occurrence002 was not rerun", "unit_return": 0}
```

## Exact contract validation record

```text
R002 contracts delegate validation
UTC date: 2026-09-16
Interpreter: C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8
Environment: PYTHONPATH=src;tests; PYTHONUTF8=1; PYTHONIOENCODING=utf-8; TMP=C:\tw18
Provider calls: 0

JSON and metaschema validation:
JSON_OK 18
SCHEMAS_OK 12 jsonschema 4.26.0

Branch fixtures (actual Draft 2020-12 validation with local external-reference store):
EXAMPLES_OK answered=11 cannot_decide=7 negative_contradictions=5

The five rejected contradictions were: cannot_decide answer with a claim; cannot_decide tested critic with an objection; cannot_decide recoding solve with a claim; cannot_decide native-match note with an answer; cannot_decide propagation use with a checker proposal. Answered fixtures covered every response/execution schema. Cannot-decide fixtures covered every model-response schema with that branch. Shape-only manifest schemas instead validated their actual files below.

Actual candidate artifacts:
problems/RECODING_MAPS.json OK 24
problems/RELATIONS.json OK 24

Recipe invariants and references:
RECIPES_OK files=6 fixed_calls=14 completion=237568 shared_use_schema=5

Schema SHA-256:
answer.schema.json c5b54d66584bbc8c25a698257171b6e0e222898615201c631ef6221d95e7cbf6
checker-execution.schema.json 5be7f778a5b6fd5f7f0990c696b3885cc9e1b35bae5061b5aec3c2c661b698a2
checker-proposal.schema.json 28ef41d4be24a3faa93c6fc8a6fa7d4e0f641050f47c49b6c485840525e3d4ad
coding-manifest.schema.json f6a2deab8fa40b60a865d1911f3abb6a7d821aa1d6b55df5e5e09172f7d5e74c
native-match-note.schema.json 78a6b008fec97c79455811c126ad8ba9fea206327ed3cc65a5dc4d4593077a25
propagation-use.schema.json 12dbef8f3ce52efc2819fe1c8be3335cd77f20156e860c504a44e1e51745fdd4
prose-objection.schema.json e81a1677a6b88617cbcfc24f0f3bef8857e80a2439375c2ba72986ee742a5839
prose-return.schema.json d4c5348d81673cbb9f9f6cdb423f31fc2bef38022649364a85be873b5a07b538
recoding-solve.schema.json d5e867b8a25931eebfa7708f21eb49f9f91d63927e1ea712b5d93c249d6d0350
relations.schema.json e005b3b510b2a7027c89a166cdc2789388c4a54a9c6aa1d6da66f8c2dab88f13
tested-objection.schema.json a3b092330c5bb807f3da54e4c069e4f370461a65db369bb3372895de4eae865f
tested-return.schema.json 302414bcb96037e3cb20535a9f3b51de6c756bb5e6ef822845beda7f7b7dcdce

Recipe SHA-256:
r002-carrier-v1.json e189ab7d961677df4dced1f29894c586c73d6696196968e0fa0e2b932357916a
r002-checker-v1.json e629fd024a4ddd950ecab947696a9dbeac653ef5c35635ae5023c315a5f932a2
r002-cross-match-v1.json 32e69459cbcdd40ab1ea01e451257a8e09be6c4a24ce2ae167007d163832f0b5
r002-native-match-v1.json 9b51f5c7f28c5b37ff7f20ec221d02c1e42878c23ba9e7e770d0d46c18c23ac8
r002-recoded-v1.json 0e6b05b72c34af2a8b01fd58a6e8324d5de325b72292455a9fa17e59d5ce56a0
r002-tested-cross-v1.json dd0a4975a9d41879998e9f969faca4fabe236c409be652570c939393dfc712f3

Limit: these are JSON/schema/contract structural checks. They do not implement the proposed engine, qualify a checker sandbox, call a provider, or adjudicate episode content.

Final shared-oracle custody repair:
problems/RECODING_MAPS.json OK 24
ORACLE_SUPPORT_OK records=24 required_fields=2 keysets_equal=24 actual_hashes=24 negative_missing=2
problems/RELATIONS.json OK 24
INSTRUMENT.md SHA-256 0246a96d2ad77d914e15b8628a6beaa3354249e09124e35b5ec23b538cb7d6e7

Final propagation-retention and refreshed support checks:
RETENTION_USE_OK answered=1 identical_query=1 unchanged_dependency_false=1
ORACLE_SUPPORT_REFRESH_OK records=24 actual_hashes=24
```

## Separate endpoint recomputations

```json
{
  "status": "PASS",
  "candidate_ids": [
    "C01",
    "C04",
    "C08",
    "C09",
    "C10",
    "C11",
    "C13",
    "C17",
    "C18"
  ],
  "checks": [
    {
      "candidate_id": "C01",
      "independently_computed": {
        "posterior_C": "25/129",
        "next_red": "224/387"
      }
    },
    {
      "candidate_id": "C04",
      "independently_computed": {
        "rows": [
          [
            "Blue",
            2,
            3,
            17,
            3
          ],
          [
            "Gold",
            2,
            2,
            12,
            3
          ]
        ]
      }
    },
    {
      "candidate_id": "C08",
      "independently_computed": {
        "spanning_trees": 1680,
        "containing_01": 900
      }
    },
    {
      "candidate_id": "C09",
      "independently_computed": {
        "matching_strings": 59,
        "probability": "4129056/244140625"
      }
    },
    {
      "candidate_id": "C10",
      "independently_computed": {
        "count": 1,
        "least": 1912,
        "sum_mod_2520": 1912
      }
    },
    {
      "candidate_id": "C11",
      "independently_computed": {
        "sequence": "FABCDEGH",
        "minimum": 26,
        "second_distinct": 27
      }
    },
    {
      "candidate_id": "C13",
      "independently_computed": {
        "count": 3120
      }
    },
    {
      "candidate_id": "C17",
      "independently_computed": {
        "P20": 510725921871,
        "coefficient_x7": -1
      }
    },
    {
      "candidate_id": "C18",
      "independently_computed": {
        "completions": [
          [
            "C",
            5
          ],
          [
            "D",
            6
          ],
          [
            "B",
            7
          ],
          [
            "F",
            9
          ],
          [
            "E",
            13
          ],
          [
            "A",
            16
          ],
          [
            "G",
            19
          ]
        ],
        "turnaround_sum": 47
      }
    }
  ],
  "scope": "Nine independent recomputations against actual sealed answer JSON; no participant call; other oracles validated by study run_all and root reading."
}
```

## Custody, scope and limits

Root syntax, UTF-8, JSON Schema metaschema, high-risk credential-pattern, exact R001 extract and 32 revised source-pin checks pass; the current machine result is [ARTIFACT-VALIDATION.json](../../../work/w18/ARTIFACT-VALIDATION.json). It never reads .env or compares actual secret values. Schema validity and hash identity establish neither semantic validity nor checker containment.

The user's as-found branch remains claude/project-state-direction-j5rbun. A concurrent publisher advanced HEAD from 65a1a45cbf1722f339682488c46d27f5ba236d72 to 0dc9182ebeb4dd350854cdbd229e5faf988d94ca and changed docs/index bytes. This task performed read-only git commands only; it neither reverted nor incorporated those external changes. See [SCOPE-CHECK.json](../../../work/w18/SCOPE-CHECK.json), [CONCURRENT-COMMIT.txt](../../../work/w18/CONCURRENT-COMMIT.txt), and the separate R001 premise supplement. Do not claim the entire shared checkout stayed unchanged.

No provider, checker sandbox, live timeout enforcement, hidden-reasoning custody or new contract execution has been qualified here. Live mode refuses even a capability marker until separate engineering implements the adapter. Unchanged legacy CROSS's repair/fallback behavior conflicts with strict no-repeat policy; its live command remains gated pending a prospective resolution, as PLAN and INSTRUMENT state. The budget retains its conservative historical maximum rather than concealing those extra attempts.

[MATERIAL_PINS.json](MATERIAL_PINS.json) freezes this draft's study artifacts except the pin file itself. Notes, earlier snapshots, operational failures and final receipts remain under [work/w18/INDEX.md](../../../work/w18/INDEX.md). No scientific comparison has run; the next task is engineering and independent review/publication, followed only by separately authorized calibration.


## W20 offline engineering verification - 2026-09-16T22:32:19.425840+00:00

REC-20260917-A. The mutable R002 implementation is tools/run_R002.py and src/minireason/reason/r002*.py with checker.py; the published draft launcher, contracts, recipes and other study files remain unchanged. This append is a completion supplement, not a rewrite of the earlier draft observations.

The final required reason discovery suite passed 212 tests (74.029 seconds); tests.loop.test_docs_pins passed 26 tests (0.018 seconds). Contracts, cannot-decide branches, actual request schema/reference delivery, strict critic/native ceilings, fork/redo binding, tail edits, recoding, stall switches, checker refusal/timeout/memory/output/mismatch/match, checker receipt recovery binding, episodes, counters and launcher resume/rerun custody are covered by offline fixtures. All seven recipe maximum-call fixtures fit the unchanged offline prompt cap; that byte counter is not a model tokenizer qualification. The independent checker receipt finding is resolved and reviewed in work/w20/checker/FINAL-REVIEW-RESOLUTION.md.

Standalone launcher calibration for C01/C02 made one synthetic native slot each. Main completed all five default conditions for both candidates: 50 synthetic slots total. These default fixtures respond cannot_decide; they execute no checker (checker_runs=0). The separate checker/engine fixture suites exercise actual isolated subprocesses and mismatch delivery. Both launcher resume commands returned zero; all 560 phase files remained byte-identical. No semantic admission judgement, live provider call, root .env read, Git mutation or sandbox qualification occurred. Source pins match the final current implementation exactly.

Exact command/output paste:

```text
COMMAND: C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 tools/run_R002.py --phase calibration --mode offline --run-root C:\Dev\miniReason\work\w20\l\final03 --problems C01 C02 --env-file C:/tw20/nonexistent-w20.env
{"mode": "offline", "phase": "calibration", "schema": "minireason.r002.launcher.v2", "scientific_evidence": false, "selected_candidates": ["C01", "C02"], "status": "COMPLETE"}

EXIT: 0
COMMAND: C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 tools/run_R002.py --phase main --mode offline --run-root C:\Dev\miniReason\work\w20\l\final03 --problems C01 C02 --env-file C:/tw20/nonexistent-w20.env --admission-receipt C:\Dev\miniReason\work\w20\launcher-admission-fixture.json
{"mode": "offline", "phase": "main", "schema": "minireason.r002.launcher.v2", "scientific_evidence": false, "selected_candidates": ["C01", "C02"], "status": "COMPLETE"}

EXIT: 0
COMMAND: C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 tools/run_R002.py --phase calibration --mode offline --run-root C:\Dev\miniReason\work\w20\l\final03 --problems C01 C02 --env-file C:/tw20/nonexistent-w20.env --resume
{"mode": "offline", "phase": "calibration", "schema": "minireason.r002.launcher.v2", "scientific_evidence": false, "selected_candidates": ["C01", "C02"], "status": "COMPLETE"}

EXIT: 0
COMMAND: C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 tools/run_R002.py --phase main --mode offline --run-root C:\Dev\miniReason\work\w20\l\final03 --problems C01 C02 --env-file C:/tw20/nonexistent-w20.env --admission-receipt C:\Dev\miniReason\work\w20\launcher-admission-fixture.json --resume
{"mode": "offline", "phase": "main", "schema": "minireason.r002.launcher.v2", "scientific_evidence": false, "selected_candidates": ["C01", "C02"], "status": "COMPLETE"}

EXIT: 0
```

Required test command/output paste:

```text
COMMAND: C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 -m unittest discover -s tests/reason -t .
Run directory: C:\Dev\miniReason\work\w20\tests\cli\20d025a9
{"run_id": "20260916T222900Z-r002-2a2095", "stop_reason": "complete", "completed_cycles": 0, "calls": 1}
{"run_id": "20260916T222900Z-r002-2a2095", "stop_reason": "complete", "completed_cycles": 0, "calls": 1}
.....................................................CONFIG_ERROR
...............................................................................................................................................................
----------------------------------------------------------------------
Ran 212 tests in 74.029s

OK

EXIT: 0
ELAPSED_SECONDS: 74.407

COMMAND: C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 -m unittest tests.loop.test_docs_pins
..........................
----------------------------------------------------------------------
Ran 26 tests in 0.018s

OK

EXIT: 0
ELAPSED_SECONDS: 0.531
```

Full custody: work/w20/INDEX.md, TESTS-FINAL.txt, DOCS-PINS-FINAL.txt, LAUNCHER-FINAL.txt, LAUNCHER-VERIFICATION.json, SOURCE-VERIFICATION.json and l/final03/. Historical final01/final02 and intermediate/failing probes are preserved and are not final-source proof. Future live calibration requires its own receipt, published engineering review capability and qualified local tokenizer pins. The detached 24-call command is in work/w20/CALIBRATION-LAUNCH.md and was not executed. Live CHECKER remains refused until a qualified OS/container backend exists; Python subprocess guards alone are not that qualification.


W20 scope correction - 2026-09-16T22:34:08.005009+00:00: The final byte-level audit found that the raw Git index hash differs from its opening fingerprint. HEAD and branch remain unchanged, and git diff --cached --exit-code --quiet HEAD returns 0: staged contents still exactly equal HEAD. W20 used only read-only Git verbs; such commands may refresh index stat-cache metadata, and exclusive attribution versus concurrent writers is unproven. No restoration or Git mutation command was attempted. Subsequent reads set GIT_OPTIONAL_LOCKS=0 and preserve the current index bytes. Earlier blanket no-Git-mutation statements mean no explicit mutating command; raw-index byte preservation was not achieved. Evidence: work/w20/INDEX-CACHE-OBSERVATION.json and SCOPE-AUDIT-INITIAL.json. This exception does not change source/test results or permit publication in this task.


## VALIDATION - independent review20 - 2026-09-16T23:14:22.590000+00:00

REC-20260917-A; root-review20. APPROVED-AS-CORRECTED for publication under the owner's addenda. This is offline engineering evidence, not model/scientific evidence. No provider/model call, root .env read or Git mutation. Full judgment, corrections, failed probes and final evidence: work/review20/REPORT.md and INDEX.md. Source stable for the final runs below.

Corrections: conclusion-only tail detection; checker redo source/output delivery; no invented dependence on equal conclusions; profiler/frame/os escape containment; reviewed runtime qualification; strict Windows provider-worker process-tree supervision; automatic source-pinned exact-wire calibration preflight; corrected Unicode tokenizer proof; exact original-prefix material validation for append-only path clarification. All have regression coverage in the final suite.

Original profiler attack created one review-owned empty directory outside child cwd before correction; preserved evidence is checker/PROFILER-PRE-FIX.json. Corrected final battery:12/12 pass, plus original profiler replay refused and independent runtime profiler/os mutation denials. Default5-second wall observed5093ms; default256MiB refused512MiB allocation. LOOP-CHECKER is runnable on this host WITH ITS DECLARED LIMITS:

Reviewed host limits (REC-20260917-A): windows-personal-python-guard-v2 is runnable on this Windows host with CPython 3.11.9 executable SHA-256 5f7b89a612c9b8af1d6456cdfcd1dbe5ca630849e79aebced9bee9a6694952ec. Each check uses a fresh empty working directory, explicit JSON stdin, a cleared environment, UTF-8, UTC and PYTHONHASHSEED=0; startup uses -P -s -S -B -X utf8. The AST allowlist permits only collections, decimal, fractions, functools, itertools, json, math, operator, statistics and sys, rejects filesystem/process/network/dynamic-import/reflection access, and is reinforced by runtime import/open/audit guards, including socket, profiler/frame and os mutation denial. Windows Job Objects limit the child to one process and 256 MiB; the host enforces a 5-second wall and terminates the job. Source is limited to 32768 UTF-8 bytes and retained stdout/stderr to 65536 bytes each. The monitor polls every 5 ms: actual termination time and temporary output size can exceed the requested limits, and elapsed time/breaches are recorded. Only one finite JSON object with the expected relation, value and derivation is accepted. Code, stdin, bounded output, exit status, elapsed time, policy and runtime hashes are retained; mismatch supplies source and output to the next return as an objection. No repository, sealed answer/oracle or credential data is supplied. This is tested containment for the owner's restricted personal harness, not OS/container filesystem or network separation, a disk quota, or a proof against all hostile Python/interpreter defects. Qualification on another runtime/host requires a new review; nonmatching live runtimes fail closed.

Capability is required by INSTRUMENT207-228 and supplied at work/review20/reviewed-engine-capability.json with exact12 schema/7 recipe digests and REC-20260917-A review reference. PLAN6 permits the qualified exact-wire alternative; calibration needs no hand-made tokenizer file. All24 corrected public-serializer prompt counts independently reproduce (940-1192); provider usage remains unobserved. Main dynamic tokenizer pins remain a separate requirement. Complete detached24-call calibration command: work/review20/CALIBRATION-LAUNCH.md; not executed.

All35 prepared seat wires carry native32768/off16384; max14-call loop completion ceiling311296. Guarantee that every possible critic fits is not established: published schema has unbounded fields; any length stop must stay censored. R001 recipe and old-contract prompt bytes match HEAD; copied actual run resumed without call evidence mutation. Historical derived report/timestamp rewrites are documented separately.

### Final reason unittest discovery

```text
..........................................................CONFIG_ERROR
.......................................................................................................................................................................
----------------------------------------------------------------------
Ran 225 tests in 71.219s

OK
Run directory: C:\Dev\miniReason\work\review20\tests\cli\357e7158
{"run_id": "20260916T230912Z-r002-80128e", "stop_reason": "complete", "completed_cycles": 0, "calls": 1}
{"run_id": "20260916T230912Z-r002-80128e", "stop_reason": "complete", "completed_cycles": 0, "calls": 1}

EXIT CODE: 0
```

### Final documentation pins

```text
..........................
----------------------------------------------------------------------
Ran 26 tests in 0.019s

OK

EXIT CODE: 0
```

### Final corrected-source offline launcher and exact resumes

```text
COMMAND: C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 tools/run_R002.py --phase calibration --mode offline --run-root C:\tr20\review20-final-corrected --problems C01 C02

{"mode": "offline", "phase": "calibration", "schema": "minireason.r002.launcher.v2", "scientific_evidence": false, "selected_candidates": ["C01", "C02"], "status": "COMPLETE"}

exit 0

COMMAND: C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 tools/run_R002.py --phase main --mode offline --run-root C:\tr20\review20-final-corrected --admission-receipt C:\tr20\review20-admission.json --problems C01

{"mode": "offline", "phase": "main", "schema": "minireason.r002.launcher.v2", "scientific_evidence": false, "selected_candidates": ["C01"], "status": "COMPLETE"}

exit 0

BEFORE RESUME: {"aggregate_sha256": "a48b38b4264ecc4e8d35fc0fa7f1ddad3000ddde4a7b0790e4ab014d7cbd02a3", "files": 310}

COMMAND: C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 tools/run_R002.py --phase calibration --mode offline --run-root C:\tr20\review20-final-corrected --problems C01 C02 --resume

{"mode": "offline", "phase": "calibration", "schema": "minireason.r002.launcher.v2", "scientific_evidence": false, "selected_candidates": ["C01", "C02"], "status": "COMPLETE"}

exit 0

COMMAND: C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 tools/run_R002.py --phase main --mode offline --run-root C:\tr20\review20-final-corrected --admission-receipt C:\tr20\review20-admission.json --problems C01 --resume

{"mode": "offline", "phase": "main", "schema": "minireason.r002.launcher.v2", "scientific_evidence": false, "selected_candidates": ["C01"], "status": "COMPLETE"}

exit 0

AFTER RESUME: {"aggregate_sha256": "a48b38b4264ecc4e8d35fc0fa7f1ddad3000ddde4a7b0790e4ab014d7cbd02a3", "files": 310}

VERIFY: {"active_source_version": 1, "conditions": ["LOOP-CHECKER", "LOOP-CROSS", "LOOP-RECODED", "LOOP-TESTED", "NATIVE"], "source_files": 199, "source_pin_equal": true}
```

Earlier standalone rerun-failed and versioned-source tests passed; focused launcher/preflight11 passed and the full final suite repeats rerun custody. The final manifest contains199 matching source pins; all five main conditions are present. Original published/preregistered bytes remain intact; PLAN and LAUNCHER contain only the permitted CHANGES append directing execution to tools/run_R002.py.


### Final corrected rerun and durable archive supplement - 2026-09-16T23:15:16.367059+00:00

The separate corrected-source rerun-failed probe also completed: failed predecessor bytes preserved; successor complete; separate rerun phase receipt; source pins equal. Full corrected run311files, rerun367files and admission copy are byte-equal under work/review20/launcher, verified in ARCHIVE-CORRECTED-VERIFY.json.

```text
COMMAND: C:\Users\darre\AppData\Local\Programs\Python\Python311\python.exe -B -X utf8 tools/run_R002.py --phase main --mode offline --run-root C:\tr20\review20-final-corrected-rerun --admission-receipt C:\tr20\review20-admission.json --problems C01 --rerun-failed
{"mode": "offline", "phase": "main", "schema": "minireason.r002.launcher.v2", "scientific_evidence": false, "selected_candidates": ["C01"], "status": "COMPLETE"}
VERIFY: {"active_source_version": 1, "archived_byte_equal": true, "archived_stop": "SCHEMA_FAILURE", "attempt_source_versions": [1, 1], "attempt_statuses": ["archived-failed", "complete"], "current_stop": "no_new_objections", "rerun_receipts": ["phase-receipt-rerun-001.json"], "source_pin_equal": true, "source_versions": 1}
```
