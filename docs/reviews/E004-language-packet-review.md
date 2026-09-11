# Independent review of the frozen E004 language packet

E004 supplies two informative but substantially unfinished representational proposals. Both already contain source quotations and item-level interpretations that the setup explicitly asked them to leave for later probing. The Lean-oriented proposal additionally embeds much of the reservation procedure. Later successes can therefore involve retrieval and use of source-conditioned construction already supplied in the packet. This limitation should be carried into the comparison while preserving the original specimens.

This review inspects [packet.json](../../experiments/records/E004-paired-languages/packet.json), [the frozen plan](../../experiments/records/E004-paired-languages/plan.json), the actual [request](../../experiments/records/E004-paired-languages/calls/call-0001.request.json) and preparation result. It makes no live model calls, changes no packet bytes and performs no Lean compilation. Static observations about intended arithmetic below are conditional readings of the supplied definitions, not successful elaboration or execution receipts. Initial correct capture remains an object of inquiry, not an admission gate.

The packet ID is `85558cab828cc4f2ae010403169473ca56e6217526690587eb165b9f71555f09`; the complete file's SHA-256 is `29958c8817f0d936e20582e83cdc5f13cb1e303de96dcae306c788caa48aa7ae`. The `languages.lean` string has SHA-256 `e57dd2fda94cdfeaa6d82c77baa8c37bf80fe02cefaf0cbc36de6d004aaa46b7`; `languages.nonlean` has SHA-256 `710391b80e9385673ba9e5143ea066b75146ebf28af2f78d72c8c9fa20a30e4a`. The packet remains `FROZEN_UNADJUDICATED`.

## Source-conditioned material is present

The setup request prohibits quotations, per-fragment translations and ready-made answers inside the declarations. The Lean preamble claims it contains no quotations or per-fragment translations, but its closing notes repeatedly quote a source clause and assign it a named definition. RSS has an explicit Interpretation section that does the same.

| Source expression present verbatim | Lean declaration | Non-Lean declaration |
|---|---|---|
| “A higher revision supersedes lower revisions” | Says the clause is represented by `greater_revision_in`; that identifier is itself inconsistent with the declared `greatest_revision_in` | Translates it into structural supersession within a booking |
| “Availability can be negative” | Says the clause is represented by `Int.sub_nat` | Translates it into a derived quantity under reservation-selecting readings |
| “Duplicate deliveries convey no additional authority” | Assigns the clause to `exact_duplicate` | Uses the same clause with a lowercase initial letter and interprets it as inert exact duplicates |
| “Different bookings need not share the same choice” | Assigns the clause to the absence of a mechanism forcing a shared choice | Discusses the same issue through accounts, readings and compatibility |
| “People may disagree about whether uncertainty should be retained” | Discussed throughout the declaration | Quoted and interpreted as accounts adopting different readings |

These are direct matches to the frozen problem or corpus, accompanied by proposed translations. This is stronger evidence of setup noncompliance than generic overlap on words such as booking or revision. There is no need to infer secret test exposure: the generator was deliberately shown the complete corpus, and the leakage identified here is from that admitted setup material into the declared later translation instrument.

The Lean definitions are also more than neutral grammar. They select undominated booking records, apply a chosen expiry/release effect, form per-booking reservation lists and aggregate bounds. RSS embeds views about duplicates, supremacy of revisions, the legitimacy of negative availability, and alternative expiry readings. These are model-supplied commitments and proposed solution organization. They are not operator-authored solutions, but they become prior supplied organization for every later arm initialized from this packet.

Accordingly, a later arm reproducing these mappings cannot by that event alone be credited with independently inventing them or translating an unanticipated source. The paired packet can still support a useful comparison of how different routes preserve, inspect, criticize and deploy the same supplied organization. This audit does not erase the contaminated passages, replace the proposals or reclassify the packet as inadmissible.

## What the Lean-oriented proposal actually supplies

WHL supplies opaque sorts for bookings, revisions, quantities and time; a record and snapshot structure; duplication, revision and liveness predicates; proposed reservation functions; bounds; and formal shapes for conjectures and refutations. A conjecture is a predicate on a snapshot. A refutation pairs a snapshot with a proof that the predicate fails there. A commitment is simply `Prop`; this does not itself record who accepts it or establish any endorsement relation.

The comments describe natural-number revision, quantity and time domains, but the actual declarations make each an opaque `Type`. Only revision reflexivity and a definition of strictness through asymmetric `revision_le` are supplied. Quantity addition, ordering and zero, time comparison, the decidability needed by computational branches, and the conversion of quantities to the `Nat` arguments of `Int.sub_nat` are not supplied by those declarations. `rules_disagree` also refers to `possible_reservations_with` before that definition appears. The file's own declaration of `Int` creates an additional potential core-name conflict. These are visible reasons that Lean-core compatibility remains unestablished; they are not quoted compiler errors, because compilation was unavailable.

Independently of elaboration, several intended distinctions are absent or different in the written definitions.

| Component | What is present | What does not follow |
|---|---|---|
| Revision authority | `greatest_revision_in` means membership plus absence of a strictly dominating record | A greatest revision in a total order is not established. The weak axioms allow incomparable revisions; they also permit three-way strict cycles, leaving no undominated record |
| Greatest-revision alternatives | Same booking, both undominated, not exact duplicates | Equality of revision is not required, so incomparable different revisions can be classified as alternatives |
| Expiry readings | `reserves_effect` and `expired_deletes_rule` have identical bodies | The latter does not remove a record before greatest-revision selection. Supplying it to the same selection pipeline cannot realize the advertised resurrection alternative |
| Availability bounds | The lower-named function subtracts the sum of booking minima; the upper-named function subtracts booking maxima | Under the stated natural-number arithmetic reading these names reverse the bounds on availability |
| Duplicate handling | An equality predicate and lists whose filters preserve multiplicity | Equality does not itself deduplicate records. Raw reservation lists can change under replay even if their minimum and maximum do not |
| Booking aggregation | The caller supplies an arbitrary `List Booking` | Uniqueness and completeness of that list are not enforced. Repeating a booking can double its contribution; omitting one can omit a reservation |
| Cross-booking uncertainty | Separate reservation lists and aggregate extrema | No explicit exact global alternative-set construction or compatibility relation is supplied. Intervals alone do not retain holes in the set of possible totals |
| Criticism and provenance | Predicates and snapshot counterexamples | No explicit account of dependence on source assumptions, delivery provenance, or the target of a rule/interpretation objection is installed |

The deletion-rule observation is exact at the text level: both functions match on record kind, return zero for a release, and for a hold return zero when `t > expiry`, otherwise its quantity. Their difference exists in names and comments, not in the proposed effect function. `deletion_changes_greatest` can describe a higher expired record together with a lower active record, but it still does not implement an alternative selection operation.

At equality of time and expiry, the proposed hold rule remains active. That is a definite choice in WHL's intended interpretation. The E004 source discusses a time being past expiry but does not settle equality precisely. It would be an error to import the earlier E001 strict-boundary contract and announce that WHL has already been refuted on this new specimen. Equality is a useful interpretation probe whose alternatives should remain visible.

Missing dedicated primitives do not prove that full Lean cannot express replication, provenance or source assumptions. Lean's ambient proposition and data-forming resources can be broader than WHL's supplied convenience definitions. A claim of inexpressibility must therefore specify whether the route permits only the declared vocabulary, arbitrary expressions formed from it, or additional Lean definitions. Adding definitions to the package is a successor intervention; using an already admitted expression form is not automatically a package revision.

## What the non-Lean proposal actually supplies

RSS distinguishes delivered records, stories supported by deliveries, viewpoints, readings, projections, accounts and open inquiry states. It includes provenance in its initial Story primitive and allows viewpoint-relative coordinates. Those provisions can express disagreements about who sees what and under which expiry or cancellation policy. It also explicitly allows criticisms of a record, rule, history, snapshot, coordinate or assumption.

Those differences are real proposed representational resources, but their interpretation is often partial or inconsistent. Exact duplication requires equal provenance as well as equal record fields. If two separate deliveries of the same immutable record have different event provenance, they no longer count as exact duplicates under this reading. Whether that creates additional authority is left unspecified; it exposes a missing distinction between record identity and delivery occurrence. Later, RSS says exact delivery provenance cannot be expressed unless provenance is added, despite having introduced it as a primitive. The relation between its generic provenance field and its claimed limitation needs clarification in a successor, without replacing the initial bytes.

Its definition of liveness first requires absence of a higher revision, while its expiry-deletion reading says that deleting the higher expired record can make a lower revision live. This can be coherent if each reading determines the effective comparison bag before liveness is evaluated, but that operation is not supplied. Likewise, one passage makes supersession depend on a reading while the Interpretation section says it holds under all readings. A representation test should ask which relation actually varies rather than choosing a reconciliation silently.

RSS's assertion of noncomputability rests on its failure to provide an algorithm for selecting readings or resolving disagreements. Absence of a supplied algorithm is not a proof that no algorithm exists, nor does it identify a precisely posed decision problem. The supported description is a non-executable or incompletely operationalized semantic proposal. Its legitimacy as prose does not depend on turning the label into a computability theorem.

The statement that every projection necessarily loses information is also stronger than its premises. A projection on a singleton admitted domain, or an injective projection at a suitably fixed grain, need not collapse any retained distinction. Particular availability projections can lose distinctions; that should be shown with a pair of cases rather than stipulated universally.

RSS initially describes refutation as a counterexample or inconsistency, then adds another account's rejection of a supporting assumption as a third form. Disagreement with a premise may withdraw that support route for the dissenting account. It does not alone establish the conjecture's falsity, an inconsistency within the first account, or failure of every supporting route. The broader word therefore merges distinct argumentative events unless its local interpretation is made explicit.

An open conjecture is defined as one no account has accepted or refuted. Thus one account's acceptance makes a conjecture cease to be open even while other accounts disagree and no decisive argument is available. That is a substantive inquiry-state choice, distinct from the proposal's broader promise to preserve unresolved disagreement.

These findings expose named commitments and ambiguity; they are not a verdict that unrestricted prose cannot express the missing distinctions. RSS leaves its statement grammar and reading space open enough that upper bounds on expressibility cannot be inferred simply by counting its listed primitives.

## Deliberate probes of the frozen declarations

The following probes inspect the initial packet unchanged. They ask an arm to represent or distinguish content using the admitted route and to preserve unresolved or conflicting readings. They do not ask it to silently fix the declarations. Each response should identify when it is quoting a supplied mapping, deriving a consequence, using ambient language resources or proposing a successor extension.

| Probe | Fixed contrast | What the comparison can reveal |
|---|---|---|
| Effect versus deletion | One booking has an expired higher revision and an active lower revision; compare the two named Lean effect functions without editing them | Whether the arm notices that identical definitions cannot implement the comments' different selection order, and whether it can retain the intended difference as a prose criticism |
| Extrema and exact alternatives | Capacity 10; booking A alternatives 0 or 2; B alternatives 0 or 3 | Exact availability is `{5,7,8,10}` under independent choices. An interval loses holes; the Lean lower/upper function names reverse their intended numerical bounds |
| Maximal versus greatest | Two incomparable revision values under the declared axioms, then a three-way strict cycle | Whether the arm uses the actual weak relation premises or silently imports the comments' natural-number total order |
| Record replay versus provenance | One immutable record delivered twice through distinct delivery events | Whether record equality, provenance, raw-list multiplicity and authority are kept distinct in each declaration |
| Caller-supplied booking list | One active booking reserving 3 with capacity 10; compare `[b]` with `[b,b]` | Under the intended arithmetic, the aggregate changes from 7 to 4. The issue is an unenforced input convention, not a claim that duplicate delivery must have this effect |
| Expiry equality | Hold expiry equals the viewpoint's current time | Whether the arm states the language's chosen convention while keeping the source's boundary ambiguity visible |
| Rejected premise versus refuted conclusion | Two accounts disagree about an auxiliary assumption while a separate support route remains available | Whether RSS's broad refutation label hides a distinction that prose or additional declared relations can retain |
| Open disagreement | One account accepts a conjecture; another challenges it without settling it | Whether the arm notices the difference between RSS's defined open predicate and unresolved inquiry |
| Viewpoint and resource dependence | Identical record fields interpreted at two replica times; then an explicit cross-booking compatibility restriction | Which distinctions the supplied primitives can carry, which require an admitted ambient expression, and which require a successor package |

For subsequent component interventions, the cleanest targets are the revision-order supply, the effect/selection boundary, interval versus exact-alternative carriers, provenance identity, and the distinction between refusal of a premise and refutation. Each intervention should name the missing or conflated relation it addresses and produce a new package identity. Removing source translation notes would be a separate deliberate leakage-control condition, not a cleanup of E004. Such conditions should keep the original paired packet and unchanged carrier comparisons available.

The immediate comparison can establish how well a route preserves and uses these particular model-supplied organizations, including their errors. It cannot establish a general Lean versus prose hierarchy, a formal proof result, or historical newness of mappings already embedded in initialization. Passing a probe demonstrates a bounded interpretation or construction under stated supplies; failure can identify a route limitation or a misunderstood commitment. Neither outcome licenses erasing the initial language specimen or treating prose as subordinate to compiler acceptance.
