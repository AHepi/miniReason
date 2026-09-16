# WAVE7 interface: exact-source contribution pairs

Implemented offline mechanism; F003 and L004/v6 remain draft proposals. No model execution or run identity is authorized by this interface.

Citation aliases: F003 = experiments/diagnostics/F003-operative-return; v5/v6 = the corresponding directories under docs/design/loop-prereg-draft-2026-09-14; F09 = experiments/diagnostics/F001-fork5-multifamily/occurrence-09.

## 1. Contract and compatibility

Set `reading_rows_builder: "pairs-v1"` in a future reviewed loop config to select this adapter. Omit the field to retain the historical H005 row path and canonical config shape. A declared unsupported value, including null, is refused as CONFIG_INVALID_VALUE. The config schema name, READ/USE_TABLE step kinds and receipt schemas are unchanged. READ still invokes the existing guarded reader; USE_TABLE still builds its original instrument output. Implementations: src/minireason/loop/types.py:1150; tools/auto_loop.py:1906.

S0 conditionally pins rows_pairs.py and all source material/arms/plan, response text, trace and artifact files returned by source_paths. The existing pin list remains unchanged when the option is absent. These are future identity inputs, not an identity minted by this work. Existing source digest values are never rewritten in a published plan. Implementation: tools/auto_loop.py:694.

The historical parser accepts the short h005-row form (tools/auto_loop.py:330). The v5 starting contract is docs/design/loop-prereg-draft-2026-09-14/v5/PREREG.md:65-83. All extensions and departures are recorded in v6/CHANGES-PREREG.md under that same directory.

## 2. Offline API

```python
from minireason.loop import rows_pairs
rows = rows_pairs.build_rows(occurrence, repo_root=repo)
index = rows_pairs.adapter_index(rows)
comparisons = rows_pairs.juxtapose(rows)
surface = rows_pairs.build_surface(rows[0])
```

These operations read local frozen files and construct values. They do not initialize an occurrence or dispatch a request. build_surface requires both source contributions; a missing contribution remains a candidate with an unresolved reason and has no fabricated surface. APIs: src/minireason/loop/rows_pairs.py:201; src/minireason/loop/rows_pairs.py:325; src/minireason/loop/rows_pairs.py:382.

Default order is mini_prose then mini_fcl, and objection->response, rival->response, response->carry within each. That gives six candidate slots for the supported frozen daily/cycle-1 material; the enumeration decides admission. A response-to-carry pair does not automatically classify the response as a criticism (v5/PREREG.md:33,65-69). A material.pair_rows declaration explicitly supplies a source tag, problem/cycle and conceptual treatment groups for F003; it supplies coordinates, never authored evidence (src/minireason/loop/rows_pairs.py:201).

## 3. Admission and source index

An ADMITTED slot has at least one exact authored later reference, a unique corresponding native selected-source mapping, matching earlier and later artifact coordinates, and matching public-text hashes. Generic phrases such as the objection are admitted only at declared whole-contribution grain through that frozen source mapping. Exact port or artifact labels come from the trace, not an invented record vocabulary. A port#record suffix additionally needs a unique exact raw authored id anchor. Missing or ambiguous record anchors remain unresolved_references; they cannot be promoted by stripping the suffix. An independent valid whole-contribution reference may still admit the slot. Implementations: src/minireason/loop/rows_pairs.py:132; src/minireason/loop/rows_pairs.py:201.

Every candidate retains its disposition, all qualifying references in source order, unresolved references, target/referring coordinates, mapping evidence and optional account context. Each exact source span includes repository path, full-file SHA-256, half-open UTF-8 byte offsets, physical line numbers, code-point coordinates and verbatim text. adapter_index checks key components, raw-key/folded-cell uniqueness and source-pair uniqueness. Alias u and ref are adapter components, not participant-authored record names. No malformed FCL is repaired or parsed into inferred relations.

A failed custody check or missing exact reference is UNRESOLVED with its reason. Admission is a source-correspondence fact. It is neither a guarded reading nor a semantic relation attributed by the instrument (FW5:626-634,640,653).

## 4. Surface and raw-byte fidelity

The Surface quotes each whole raw response.txt contribution once, including original escapes, fences, Unicode and CRLF. Exact short passages remain located by the adapter's byte/line spans within that unchanged text. This explicitly departs from duplicating short excerpts alongside whole contributions in v5/PREREG.md:73-75, because duplicate quotes can obstruct the existing unique-substring guard. Authored uptake remains visible in the original text; the adapter does not infer an enacted permission from it (FW5:638-653). Implementation: src/minireason/loop/rows_pairs.py:325.

Declared regions use pair-referring and pair-target sides. Their source_field is raw_utf8_text; file offsets remain code-point offsets, matching the existing Surface resolver. Legacy Offset.source_field is None for these new sides, so it cannot falsely name a JSON artifact field. raw_offset proves the separate UTF-8 byte correspondence against the original full-file hash. Source: src/minireason/loop/rows_pairs.py:366; src/minireason/loop/surface.py:752-759.

Account context and withheld archival criticism are labelled context and excluded from operative regions. Scaffolding is never a quotable operative region. Existing G2 uniqueness and G3 containment guards operate unchanged (src/minireason/loop/surface.py:762).

## 5. F003 same-position comparison

The proposed F003 native template maps RETURNED, ARCHIVED, RECODING, CHANGED and CARRIER branches within each Mini/matched runner arm. A shared actual objection can reach one branch while remaining outside another branch's response/use ports; native same-arm routing motivates this layout (experiments/diagnostics/F003-operative-return/PLAN.md:13-17,37-49).

juxtapose groups the same pair position within one runner arm and preserves declared treatment order, source keys, separate surfaces and each unresolved disposition. It exposes comparison material to an operator/reader; it does not create automatic cross-case marks or invoke a judge. The driver READ path reads only the declared admitted keys (src/minireason/loop/rows_pairs.py:382; tools/auto_loop.py:1906).

For ARCHIVED objection->response, the raw objection appears only as labelled archive context and is excluded from operative target regions. That candidate remains UNRESOLVED; withheld content is not a delivered target. A conflicting trace is separately recorded as an archive-route conflict. The final F003 proposal has no generated rival node, so all ten rival candidate slots remain unresolved when that topology is used. No rows are fabricated for the unrun draft. The draft has thirty candidate positions and zero available observations (F003/PLAN.md:49).

The inherited candidate and household codebook are operator enabling contributions; generated transformations remain fallible proposals. Literal full-envelope equality is not claimed because the frozen renderer exposes different coordinate banners. Owner review must resolve that limit before dispatch (F003/PLAN.md:13,23-31,53-57).

## 6. Keys and Windows boundary

F09 keys retain `h005-row/<a><l>#u/ref/<e>`. F003 adds a short declared source/treatment tag, such as `h005-row/dpRr#u/ref/o`. Key components map one-to-one to source coordinates and spans, and collisions are rejected across the driver's occurrence set. Folding agrees with auto_loop.cell_key_for. No digest suffix is treated as a mathematical guarantee of injectivity; actual keys are checked.

At the proposed L004 run name under C:\Dev\miniReason\experiments\loops, the longest initial full provider path is 189 characters for F09 and 193 for declared F003 keys. Original, order-swapped and paraphrase paths are computed; a path reaching 240 is refused. These are computed strings, not created provider directories. Reopening path allocation remains a separate unresolved launch condition. Computation: src/minireason/loop/rows_pairs.py:81; v6/reading_set.json:path_length; work/w11/rows-f003-draft.json.

## 7. Evidence and semantic limits

Occurrence-09 admits all six candidate slots, with zero unresolved slots and no unresolved identified record references. Exact passages and hashes are in v6/reading_set.json:candidate_rows and work/w11/rows-occ09.json. Prior exposure is declared; the result is not a source-blind prediction. The prior zero-row H005 table remains unchanged (experiments/loops/L003-loop-first-live-2026-09-14/cycles/cycle-01/use-table/occurrence-09/USE_TABLE.md:93-106).

FW5 requires active nonconstant dependence, not an archived dead branch (FW5:589-601). Reason use requires an interpreted role-preserving organization and its content/recoding/carrier contrasts, not just an explicit reference (FW5:626-634). K2 standing and usability are not certified by declared dependencies (FW5:638-653); a passing mechanical check is no truth authority (FW5:655-672). Build differs from transfer (FW5:714-720), historical New needs the whole prior repertoire (FW5:728-750), Origin requires Attempt, New and Build together (FW5:756-764), and a critical episode need not end in improvement (FW5:771-777). All FW5 citations identify docs/sources/FW5-explanatory-construction.md.

Later guarded readings are judge-role artifacts. This adapter does not establish those semantic conditions, compare model standing, or discharge obligations. Unresolved never means absent. Open launch decisions remain F003 envelope/candidate review, F003's own receipt and delivery, then L004 source/budget/pin freeze plus the inherited O5, stop, scoped-ceiling and actual-call accounting issues (v6/CLONE-PATCH.md).

## Independent judge contract corrections

Explicit port references are checked as complete tokens. An extended name or malformed repeated record suffix remains unresolved with its exact token retained; a shared hash prefix inside a different identifier cannot admit a source. The exact short displayed hash or full hash must occupy its own token. This prevents source-name repair by truncation.

Native matched direct traces use visible_sources and direct_explicit_views, with no Mini projection_artifacts (runner v2:1237-1254). The adapter uses that original mapping and verifies the exact selected-source header and original_brief hash. It invents no projection artifact. Both fields must have been exposed for this whole-contribution adapter; narrower views remain UNRESOLVED. These additions are covered by the corrected matched fixture and token/custody regression tests in tests/loop/test_rows_pairs.py.

Reference-token boundaries conservatively treat non-ASCII UTF-8 bytes, slash and colon as identifier continuation. They cannot terminate a matching ASCII record prefix; a malformed extension remains unresolved with its original token retained. Whitespace, quotes and brackets delimit the ordinary displayed references. This policy can leave a punctuation-ambiguous reference unresolved; it never repairs it into a shorter name.
