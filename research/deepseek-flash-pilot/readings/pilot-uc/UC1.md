# UC1: Blender blocking

Reader: root-w43, current Codex/OpenAI reader, cross-provider relative to DeepSeek; no independently logged exact reader variant or blindness claim. Read attempt4 answers before opening the four sealed briefs; task files and READING expectations were already exposed. All four brief hashes matched their manifests. The pilot received pinned task sources, not these briefs. This is an offline substantive reading, with no provider/model call, Blender execution, product test, Git mutation or run write. Historical reading sheets remain unchanged.

Authority: [amendments](../../AMENDMENTS.md), each run's own RUN.md, TRACE.md, pass files and choice events. Exact artifacts and all current decisions are in [OWNER-READING](OWNER-READING.md); all sixteen attempts and every decision verbatim are in [INVENTORY](../../../../work/w43/INVENTORY.md). [Custody](../../evidence/uc/CUSTODY.md) binds the original run files.

**Partly usable: the shot specification is a concrete blocking brief; the script is not usable as supplied. No completed self-repair was observed.**

## Artifact against the owner purpose

The [shot specification](../../evidence/uc/UC1/a4/shot-spec.json) declares three cube subjects, dimensions and initial positions; 24 fps, 1920x1080; S01 frames1-96 at28mm, S02 frames97-168 at50mm, S03 frames169-240 at35mm; courier approach/turn/retreat, a fixed crate and a descending drone. These are usable instructions for a video-generation operator to build reference staging, key poses and timed camera views. The literal embedded SHOT_SPEC matches the returned JSON by value. This is plain bpy, not evidence of using the owner's requested latest Blender plugin: no particular plugin was named or invoked.

The [script](../../evidence/uc/UC1/a4/blocking.py) cannot be accepted by inspection:

- `key_transform(obj, "rotation_euler", motion["frame_start"], math.radians(0.0))` passes a scalar to a three-component Euler property. Its helper performs `setattr(obj, data_path, value)`. That is also forbidden reflection under the task's explicit narrow grammar. A scalar does not implement the declared `[0,0,0]` to `[0,0,0.7853981633974483]` rotation. No runtime execution was performed.
- `look_at(camera, [-4.0, -6.0, 2.8])` and `look_at(camera, [7.0, -10.0, 2.0])` aim at camera positions instead of the specified shot targets. They execute before the corresponding location assignment, and camera rotation is never keyframed. Only the last assigned orientation remains; the three intended framings are not built.
- Camera location/lens keys exist only at starts1/97/169. No end holds or constant interpolation implements distinct stable shots. On ordinary Blender animation behavior this gives movement between starts; exact visual framing is unverified.
- The script creates subject placeholders and timing, but no warehouse set, lighting or rendered video. S01's drone exclusion is asserted in prose without a visibility mechanism or a demonstrated camera-space exclusion. The allowed grammar itself does not expose hide controls, so this is not fixed simply by requesting one.

The named API target is Blender 5.2. The callable names are mostly in the repository's pinned [API allowlist](../../usecases/UC1-blender-blocking/inputs/API-ALLOWLIST.md); naming valid calls does not fix wrong value shapes or scene construction. Official versioned pages could not be fetched during this reading (402), so compatibility is limited to static inspection against that local pin. The conjunction in sealed UC1 requires shot constraints, the standalone AST/API check and a fallible review. Only the structural checker ran; neither of the latter receipts exists. Its own result says: **"Standalone AST/API verification and fallible review remain required before conformance."**

Judge43 subsequently ran the pinned standalone checker offline on the exact copied spec/script. It returned `ok: false` with `"banned name: setattr"` and `"unapproved direct call: setattr"` ([transcript](../../../../work/review43/UC1-STATIC-CHECK.txt)). This later static check confirms the grammar defect; it is not a check performed by the live run and does not execute Blender. The script remains unusable as supplied.

Against the sealed brief, the machine-readable timing/spec requirement is found, while runnable grammar, camera/subject behavior and the acceptance conjunction are missed. No render success is invented. An operator can use the spec to prepare blocking manually, but cannot hand this script straight to the named API and rely on it.

## Piloting and actual changes

Four reached passes;13 logical reservations (12 dispatched logical calls),18 physical attempts; one completed outer direct_answer child at depth1, maximum outer fan-out1, no nested leaf or synthesis. Pass1 proposed `decompose_synthesize` because a direct answer **"would under-serve the multi-part build-and-verify structure"**; the host replaced it with direct_answer. This is evidence of a sensible model proposal, not free first-pass routing. Source: `runs/pilot/UC1/events/a0003.json` and its outcome.

Pass1 structural verification agreed. Its authoritative decision continued, correctly explaining the verification limit and identifying camera targets and missing rotation keys. The strongest diagnosis is **"camera targeting is wrong in the script"**. It did not deliver a fix. The sole successful same-call repair at c0003/a01 changed `source_refs` from two unauthorized unit hashes to `[]`; the entire answer string was identical to a00. That is delivery repair, not scene repair.

Pass2 changed the route to engineer_patch; passes3/4 kept it while proposing narrower input overrides. Yet `allowed_files`, `documents`, `behavior_contract` and `test_commands` were empty in the sealed task; engineer_patch requires them nonempty, and `_validate_scope` prevents changing them. Repeating that route under unchanged authority cannot satisfy admission. The model's later plan to preserve those exact fields preserves the obstacle. Additional repair packets also confused source-read placement and compact/full input shapes. Passes2/3/4 ended in spawn output-length failures at4,096 tokens; no changed child was admitted.

Every recorded CONTINUE (passes1-3) cites the exact latest verify reference and distinguishes unavailable verification from substantive failure. It then overstates the remedy: the spec's Euler values are already radians, so **"radians computed from the spec"** would need care to avoid a second conversion. Cube size1 plus scale equal to dimensions is not shown defective; the pilot's concern there is a request for confirmation, not an established bug.

There is no before/after repaired artifact: the final answer is still pass1. The fourth decision was never dispatched. Its preflight found2,708,239 wire bytes and total bound2,720,527 against1,000,000. Earlier failure receipts embed full request records and enter later control packets; this is host-carried context growth, not demonstrated provider context exhaustion. Stop cause is `INPUT_WINDOW_EXCEEDED`, not own STOP, identical-pass refusal, USD 6 or300-call ceiling. Remaining allowance was287 calls and USD 5.764207944 estimated.

More loops plausibly could help a bounded camera/vector repair, because the defect is concrete and already diagnosed. These loops did not help the artifact: after pass1, USD 0.221591400 estimated bought unsuccessful continuation delivery. A valid repair route is the missing bridge; merely asking for more passes repeats an inadmissible action.

## Recurrences and protections

[Register](../../../../docs/lessons/harness-lessons-2026-09.md): L15/L20 recur in expanding repair/context envelopes. L21 is an applied safeguard: the declared byte bound refused the oversized continuation before dispatch, with no demonstrated undercount; L7/L19/L50 in input-shape/admission failures; L43/L49 in structural success failing to establish a usable scene; L53's verification-linked decision and budget guards remain enforced, but do not establish executable or well-judged continuation. L48 warns against crediting suggested changes without checking losses. L22/L31/L40 protections are visible: wire/usage/length prefixes survive, preflight is separately recorded, and failed attempts were not erased. No hidden-reasoning text, shell authority or execution-success claim was observed.

## What each attempt reached

| Attempt | Passes reached | Logical calls | Stop cause | Recorded continue_or_stop |
|---|---:|---:|---|---|
| 1 | 1 | 2 | OUTER_INPUTS_MUST_MATCH_SEALED_TASK | None |
| 2 | 2 | 7 | CEILING_HIT | CONTINUE |
| 3 | 3 | 10 | INPUT_REFERENCE_INVALID | CONTINUE, CONTINUE |
| 4 | 4 | 13 | INPUT_WINDOW_EXCEEDED | CONTINUE, CONTINUE, CONTINUE |

