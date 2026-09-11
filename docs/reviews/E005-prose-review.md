# E005 independent review of the frozen prose comparison

E005 contains four completed direct-arm observations and two Mini preparation failures. It shows that prose can preserve this prose source exactly, that paraphrase can retain much of its organization, and that later reading and criticism can introduce both useful distinctions and unsupported diagnoses. It does not compare Mini's reasoning machinery with the direct controls: neither Mini arm reached a model call.

This review reads the complete expression, reinterpretation and criticism texts in [E005](../../experiments/records/E005-frozen-prose/REPORT.md), the actual requests, and the frozen E003 corpus carried in its [packet](../../experiments/records/E005-frozen-prose/packet.json). It compares selected occurrences directly rather than using a fidelity score. No original bytes, source code or proposed language were changed, and no live calls or compiler runs were performed. Correct capture is an observation to investigate, not an admission gate for retaining a carrier or conjecture.

## What each condition delivered

| Arm | Completed calls | Observed expression and continuation |
|---|---:|---|
| Bare | 1 | A compressed source account plus substantial language commentary; it marks a prose escape despite already using unconstrained prose |
| Native direct | 1 | The entire problem statement and corpus text appear verbatim inside a short wrapper |
| Matched | 3 | A close paraphrase, a reader explicitly lacking the source field, and a critic with the full packet |
| Matched native | 3 | An exact copy of the corpus text, a new interpretation, and a substantial criticism of both the interpretation and the language packet |
| Mini | 0 | `MINI_MANIFEST_INVALID`: the complete serialized packet exceeds the schema's `problem` length allowance |
| Mini native | 0 | The same manifest-length rejection before any model call |

The [summary](../../experiments/records/E005-frozen-prose/summary.json) records `OBSERVATIONS_RECORDED` for the direct conditions, not a semantic pass. The Mini failures are failures of this packet-to-manifest preparation route. They say nothing about what the model would have expressed through Mini or about the expressive adequacy of prose. Using a supported source-artifact route later would create a separately identified operational comparison; it cannot replace these zero-call observations.

The one-shot and three-call conditions expose different activities. Their last outputs are respectively an expression and a criticism, so comparing only the final field would compare different jobs. The source expression must remain distinguished from its later reader and critic. There is one realization per condition, and actual token use is unequal. Native completion counts include hidden reasoning that was not available for this review.

## Exact copying is a positive fidelity control

The [matched-native expression](../../experiments/records/E005-frozen-prose/matched_native-r01/calls/call-0001.response.json) equals `packet.corpus.text` character for character: 11,731 characters with SHA-256 `6350476770ae813c186d8e2e4b434f7481216f146e5a5f3db5689c982665e6c3`. The [native-direct response](../../experiments/records/E005-frozen-prose/native-r01/calls/call-0001.response.json) contains the complete problem and text strings unchanged, with headings and an obstruction note added around them.

These observations preserve the source's competing expiry interpretations, criticism targets, dependence on assumptions, uncertain modality and explicit preference for keeping disagreement visible. They also preserve the source's errors and overstatements. For example, copying its conjecture that any single-number projection loses information does not establish that universal claim. The assigned job was to preserve the specimen, not repair it.

At the occurrence level, exact copying is enough to rule out a lost word, reordered paragraph or changed assertion inside the copied field. It does not establish understanding, independent reconstruction, operative use or historical newness. The distinctions were already supplied in initialization. Nor does identity of `corpus.text` prove that every other packet field was reproduced; the matched-native expression does not separately copy the problem statement or language declarations.

The reinterpretation request omits the original corpus field, but in the matched-native condition the complete corpus survives inside `Actual expression`. Field withholding therefore does not withhold the source's informational content in that condition. This is an anticipated copying control, not a blind recovery of absent information. Its reader can study the exact text but cannot independently verify its provenance or byte identity without the source comparator.

The request also warns that reconstruction from source quotations does not establish successful expression in a selected language. For a restrictive candidate language, quotation can bypass the tested representational resources. Here the selected carrier is unconstrained prose and the source is prose. Copying is itself an admitted carrier witness. The warning must not be transformed into a blanket rejection of prose copying or a claim that a non-copying translation is required before prose is legitimate.

## The nonnative expressions preserve content but add framing

The [bare response](../../experiments/records/E005-frozen-prose/bare-r01/calls/call-0001.response.json) retains the main booking/revision account and summarizes the ten disagreement areas. Its compression largely removes the corpus's detailed conjecture–criticism pairings and the explanation of why structural supersession is better supported while the deletion reading remains live. “The disagreements are not settled” preserves uncertainty but does not fully preserve that defeasible asymmetry of support.

Much of the response instead inventories WHL and RSS. It labels the source's opening sentence `PROSE-ESCAPE` because the two candidate languages take different primitives. Those differences may matter in candidate-language conditions. They do not establish an obstruction in the current unconstrained prose carrier, which can reproduce the sentence directly. This is a conflation of commentary about the candidate languages with the selected route. The quotation remains legitimate material even though the stated reason for classifying it as an escape is unsupported.

The bare response also declines to report the visible forward-reference concern as either an error or success because the language is frozen. Freezing prohibits silently installing a repair; it does not prohibit a clearly scoped static criticism. Compiler acceptance remains unobserved, but the missing or inconsistent declarations can still be named as hypotheses about that bridge.

The [matched expression](../../experiments/records/E005-frozen-prose/matched-r01/calls/call-0001.response.json) preserves considerably more of the source's organization. Its ten disagreements occur in the same order as the corpus's explicitly ordinal paragraphs. It carries the source's preference for structural supersession, the continued admissibility of deletion, and the conditional difference between supersession and cancellation. It also keeps the distinction between criticism of a rule and criticism of a record.

Its title, “Rival-Story Semantics for a Replicated Warehouse Snapshot,” borrows the name of the candidate RSS even while the body says that RSS is not obligatory. That is a framing ambiguity; it is not proof that RSS's operative rules were installed. The final language commentary is headed separately and contains judgments beyond simple source reproduction. Some near-quotations are not exact: “manufacturing authority” substitutes for the source's “it manufactures authority.” This small change does not itself erase the criticism, but exact quotations and attributed paraphrase should not be conflated.

The absence of the exact phrase “which source assumptions an account depends on” is not sufficient to establish loss of dependence. The expression explicitly connects the lower-release conclusion to supersession and its rival conclusion to a cancellation rule. To demonstrate a lost dependence, a critic must identify a missing binding or conditional use, not merely an omitted string. If preserving every source field is intended, the probe should name those field obligations explicitly before comparing outputs.

## Source-withheld readings add their own assumptions

The [matched reader](../../experiments/records/E005-frozen-prose/matched-r01/calls/call-0002.response.json) correctly says it cannot independently check the expression's claims of source fidelity without the original. That limitation is built into its request. It does not become a reading error merely because the subsequent critic has the full packet.

The reader goes further than that warranted uncertainty. It treats a ten-item structure as suspiciously tidy, treats alternating conjecture and criticism as implying equal evidential weight, and suspects that reported preferences may be laundered endorsements. Those are possible general concerns, but the frozen corpus itself enumerates ten disagreements, pairs conjectures with criticism, and calls one expiry reading better supported. The available comparator therefore defeats several proposed diagnoses of translator-imposed structure. Headings and grammatical structure also do not contradict the instruction to use unconstrained prose; unconstrained does not mean structureless.

The [matched-native reader](../../experiments/records/E005-frozen-prose/matched_native-r01/calls/call-0002.response.json) retains the central competing readings and correctly identifies substantial unresolved questions. It nevertheless converts the source's explicit conjecture that the snapshot is a merge into the stronger statement that the source assumes it is a merge. It calls several provisional readings central semantic claims and imports a meta-assumption about faithfully paraphrasing a source whose grammar and semantics are withheld. That last point concerns the reading task and evidence access, not a premise of the warehouse account.

The reader says it sees no source-language quotations and describes apparent rule statements as likely glosses. Without the comparator it cannot certify quotation identity. The exact-copy check shows why its confidence should remain limited: the full expression was source text, even though it was not framed as a block quotation. Absence of quotation marks does not demonstrate independent reconstruction or absence of copied content.

## The critics find real issues and also overreach

The [matched critic](../../experiments/records/E005-frozen-prose/matched-r01/calls/call-0003.response.json) usefully checks the quotations and ordinal structure against the packet. It recognizes that the conjectures and preference language were generally preserved rather than invented. But it repeatedly treats the reader's deliberately restricted visibility as a defect: the reader could not verify the source, while the critic can. Additional evidence resolves the uncertainty; it does not retroactively make the earlier evidential qualification wrong.

The critic also announces several substantial losses and then acknowledges within the same sections that those contents were preserved. Its final claim that a heading for ten explicitly enumerated disagreements imposes an unlicensed taxonomy lacks a demonstrated changed relation. More concretely, it attributes the phrase “considered under the viewpoint's reading of expiry” to the matched expression. That phrase is absent there and occurs in RSS's declaration. This is an artifact-attribution error: a criticism aimed at one occurrence uses words from another.

The [matched-native critic](../../experiments/records/E005-frozen-prose/matched_native-r01/calls/call-0003.response.json) identifies the exact copy and supplies several substantive packet criticisms. It notices the opaque numeric types, the bound reversal under the intended arithmetic, identical effect/deletion functions, replay-sensitive reservation lists, the provenance inconsistency and RSS's premature loss of open status after one account commits. These correspond to identifiable definitions and relations, not simply a demand that the specimen compile or match a checklist. Several agree with [the independent E004 review](E004-language-packet-review.md), although agreement alone does not establish their grounds.

Its stronger conclusions require correction. A `Snapshot → Prop` conjecture can close over or quantify a rule; the type alone does not prove that rule criticism is inexpressible. A per-record effect function does fail to change the selection pipeline, but that is a narrower statement about the provided mechanism. RSS's refusal to choose or rank readings does not automatically prevent an account from representing a substantive comparison of their support. A provenance difference failing the declared duplicate test does not alone establish that additional authority is awarded; the authority route would have to be shown.

The critic also treats the source's conditional “or none is true” remark as requiring a zero alternative for a single active hold. The source introduces that possibility in discussion of tied alternatives and explicitly qualifies it by the interpretation of truth. A useful probe can compare a reading admitting a null alternative with the current reservation list. The source does not require every single-hold case to include zero. Installing that change universally would add a commitment while purporting to restore uncertainty.

Finally, compiler-bridge diagnoses remain static arguments. Neither this critic nor this review has a Lean elaboration receipt. Several proposed fixes may address visible problems, but E005 installs none and tests no repaired language. The records support criticism and proposed construction; they do not establish a completed semantic repair or a successful compiler bridge.

## What this experiment adds

The strongest observation is the separation between preserving an occurrence and interpreting it. A byte-identical source can enter a later reading that hardens conjectures, changes the apparent role of an assumption or misidentifies its evidential access. A later critic can correct some such shifts while introducing a new artifact attribution or unsupported impossibility claim. Exact custody therefore supplies a useful control but does not settle representation-preserving reason use.

E005 supplies no Mini advantage or disadvantage beyond the concrete preparation failure. It does not decide which candidate language is more expressive: neither was obligatory in this prose condition, and both arrived with source-conditioned mappings already embedded. The next comparable operational run should preserve the source packet and stage purposes while making the packet available through a supported Mini route. Later component probes can then test the specific distinctions identified here without treating correct capture, compiler acceptance or absence of copying as initial admission requirements.

All proposed amendments remain outside the frozen originals. The useful outcomes are the copied-carrier witnesses, the particular interpretation shifts, the criticism mechanisms and the missing Mini observation. None by itself establishes creativity, historical newness or defeat or confirmation of ECS.
