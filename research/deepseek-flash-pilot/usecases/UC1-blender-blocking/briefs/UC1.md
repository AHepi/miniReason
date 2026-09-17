# UC1 sealed expectation: Blender blocking

Written before any owner-task run. The pilot must return both an exact JSON shot specification and a `bpy` script that embeds that identical specification.

Expected constraints:

1. Blender target is the official 5.2 Python API, 24 fps, 1920x1080, frames 1-240.
2. The only subjects are cube placeholders `courier`, `crate`, and `drone`, with the fixed dimensions and initial positions in `inputs/shot-spec-positive.json`.
3. S01 is frames 1-96 (4 s), a 28 mm wide establishing shot. Courier moves [-5,-4,0.9] to [-1,-1,0.9]; crate is fixed; drone is not a named visible subject.
4. S02 is frames 97-168 (3 s), a 50 mm medium over-courier reveal. Courier turns 45 degrees over frames 97-120. Drone descends [0,2,7] to [0,2,4] over frames 121-168. Crate remains fixed and visible.
5. S03 is frames 169-240 (3 s), a 35 mm low wide three-subject shot. Courier retreats [-1,-1,0.9] to [-4,-3,0.9], while drone descends [0,2,4] to [0,2,2.5]. Motion is continuous from S02; crate remains fixed.
6. The script clears the scene, sets timing and resolution, creates all three placeholder meshes and a camera, and inserts transform/lens keyframes. It uses only `bpy`, `mathutils`, and `math`; no file, process, or network access.
7. Acceptance is a conjunction: shot constraints pass, the standalone AST/API allowlist check passes, and a fallible review call reports no unresolved high-severity mismatch. Structural pilot-checker success alone is insufficient.
8. After each verification, the pilot records a continuation decision and reason. It continues when any hard check fails or a review issue remains; there is no loop-count cap, only the declared 300-logical-call ceiling and its stop rule.

Trap/superficial outputs include: a prose shot list without machine-readable fields; three cameras or shots with unspecified timing; visually plausible motion that breaks exact frame continuity; a script that does not embed the supplied spec; invented Blender API names; unapproved imports or I/O; a claim that Blender rendered successfully; declaring completion after the structural checker while omitting AST or review; or silently substituting a plugin the owner did not name.

No Blender execution is expected. Passing the static verifier establishes only syntax, exact constraints, embedded-spec identity, the pinned name allowlist, and absence of listed I/O surfaces. It does not establish runtime or visual quality.
