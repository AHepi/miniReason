# Operational errata

## OPS-001 — Missing schema dependencies on first extraction check

The first attempt to import the extracted Mini package encountered a missing `jsonschema` dependency in the environment. No model call occurred. Installation of the declared `jsonschema==4.25.1` and `referencing==0.37.0` dependencies resolved the import boundary; the full extraction suite is checked separately. This was environment setup, not evidence about Mini's reasoning.

## OPS-002 — Public provider discovery request timeout

An unauthenticated probe of `https://api.deepseek.com/models` timed out. The `/v1/models` route returned an authentication failure without a key and succeeded with the authorised credential, listing the intended `deepseek-flash` model. Cause of the first timeout remains unknown. No inference request or template experiment was made by these discovery calls.

## OPS-003 — Extraction dependencies and optional module catalogue

Initial extraction tests exposed historical fixture dependencies and an optional open-kernel catalogue pointing at modules that were not part of the standalone dependency closure. Required fixtures were isolated as test-only history, the retained module catalogue was corrected, and 435 inherited tests plus three standalone gates passed. A wheel installed outside the checkout compiled a manifest using packaged data. See docs/sources/extraction-provenance.json and extraction evidence. No original experiment template reuses a historical fixture.

## OPS-004 — Provider failure-record and validation gaps caught offline

Independent mocked tests exposed missing terminal evidence for non-text replies, missing or invalid usage accepted as complete, and incomplete credential-echo screening in metadata and coordinates. The adapter now records all these failures, validates nonnegative integer prompt/completion counts, and redacts retained data. Redirects are refused to keep the key at the declared destination; call sequence allocation is locked. All 23 mocked provider tests pass after correction. No experiment inference was involved. Updating the HTTP helper briefly left test mocks at the previous function; that test invocation was interrupted and the mock target repaired before verification.

## OPS-005 — Baseline reader signature error found by integration check

Before any live call, the complete mocked six-arm integration found that the direct-arm reader passed a second positional argument to the inherited strict JSON reader, whose signature admits only one. Mini arms were unaffected, so failing to detect this would have invalidated the essential comparison. The adapter call was corrected and the integration test rerun. This was a driver defect, not a model result.
