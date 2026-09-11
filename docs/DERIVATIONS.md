# Conditional propositions about Mini and the experiment

These propositions connect the current architecture to the ECS attribution conditions. They separate deduction from empirical premises. None proves that a model is creative. The relevant sources are ECS §§2.2, 5.1–5.4, 6.1–6.3 and 9.1–9.4, together with the actual request construction in `src/minireason/provider.py` and the ports in `src/minireason/templates.py`.

The architecture inspected here sends a system message containing the output contract and a user message containing Mini's rendered brief. Model, thinking mode, response format and completion ceiling are also request fields. Local stage/cycle coordinates are recorded separately and are not sent as independent API fields. Native reasoning text is not returned to later calls by this client. These are client-code facts. They do not establish that the remote provider has no hidden state.

## P1. Any effect on generated answers must cross an effective input path

Let H_i be the local history before call i. A frozen Mini configuration constructs an effective request R_i = C(H_i). Let K(y | R,z) describe the provider's response distribution conditional on the request and relevant provider state z. Deterministic execution of returned programs can produce feedback F_i, which the controller may include in later histories. The final generated answer is Y.

Assume the model receives information from this system only through its effective request and admitted tools; local graph objects have no additional channel into the provider; and all output selection being studied is included in C. Then any Mini intervention that changes the distribution of Y must change an effective request, an admitted tool/feedback result, or the selection of the returned output, unless it changes provider state z.

The proof follows the causal paths. A local difference with no path into a request, a tool observation or the final selection leaves those inputs unchanged. Conditional on the same provider behavior, it therefore leaves the generated-answer distribution unchanged. A hidden artifact can affect a report about the graph without affecting Y; the claim names generated answers, not every repository output.

This does not make Mini redundant. Constructing which evidence reaches which call, when an objection is revisited and which result is retained can be the entire useful contribution. It does prohibit attributing an extra effect to 'the graph itself' once every operative input and output-selection consequence has been held fixed.

The mapping is defeasible. Discovering an unrecorded retrieval path, an implicit conversation identifier, mutable server session, omitted response setting or graph-dependent output selector would show that C did not describe the actual interface. Inspecting source and request receipts can test the mapping; a diagram alone cannot establish it.

## P2. Equal effective requests imply equal conditional response laws, not equal samples

Assume the provider implements the same conditional kernel K in both arms. If R_A = R_B and z_A = z_B, then for every response set B:

P(Y_A in B | R_A,z_A) = P(Y_B in B | R_B,z_B).

This follows by substituting identical arguments into K. It is a conditional identity, not a claim that two calls produce identical bytes. Independent samples may differ even when the conditional laws coincide. A supplied random seed does not prove determinism, and this transport supplies no seed.

For multi-call systems, two controllers that construct the same next request from each corresponding history and apply the same deterministic tools induce the same transcript distribution, provided they share the same provider kernels. Induct on calls: the initial request agrees; the response law therefore agrees; identical transition rules produce the same next-request law. This proves a distributional equivalence of the specified controllers, not equivalence of a live adaptive controller and a frozen sequence of historical prompts.

Provider load, routing, model updates, account state, cache behavior or omitted controls can violate the premises. Matching message text alone does not match model, native reasoning, response format, token allowance or other effective inputs. Interleaving arm order and recording returned identities help diagnose such alternatives but do not reveal all remote state. A reproducible difference under apparently equal requests challenges those premises or the measurement; it does not refute the conditional equality.

## P3. A written criticism without an operative path cannot establish reason use

Let c be a recorded criticism. Suppose replacing its content changes no later effective request, tool invocation or final program selection. Under P1's premises, the replacement leaves the generated outcome distribution unchanged. Hence the record supplies no nonconstant dependence of that operative outcome on the represented distinction in c.

ECS §§5.1–5.2 requires such dependence on an active route for reason use. Recording c or mentioning its identifier cannot discharge that requirement. This is stronger than checking that a criticism kind exists and weaker than declaring that the model never reasons: it concerns this occurrence and this operative result.

Adding a port can establish availability. It still does not establish content use. The useful contrasts preserve the objection's meaning while recoding its wording, then change its relevant content while preserving irrelevant presentation. The operative response should track the declared deliberative rule. These tests can defeat a proposed representation/use mapping; finite successful probes support only the declared contrasts.

## P4. Interface success and explanatory bearing are independent obligations

Let S be the Mini submission-format predicate and A the ECS accounting predicate under a fixed interpretation. A schema-valid record can contain an unanchored explanation or a program that violates the question contract. Thus S does not imply A. A valid Mini submission with a prose body and commitments containing `[]` has the required wrapper but fails the reservation output obligations.

Conversely, under a representation-preserving recoding, the same explanatory organization can be expressed in prose that lacks Mini's mandatory wrapper or executable commitments. ECS fixes content and role relations, not that transport syntax. If the account survives the recoding but S fails, A does not imply S. This argument assumes the recoding really preserves the represented organization at the fixed grain; that assumption is criticizable under P1 of ECS's primitive registry.

Accordingly, a failed machine reading may defeat an interface claim while leaving the original prose account unresolved. An exact program pass may establish bounded behavior while its accompanying explanation has no bearing. Both records need separate review. Neither the format checker nor an overall prose score can substitute for the missing relation.

## P5. Finite task success cannot alone establish historical newness

ECS §6.2 requires that no prior deployable content equivalent to c at the fixed grain existed in the system's repertoire. A finite collection of successful API outputs observes current behavior, not that entire earlier repertoire.

Consider two histories compatible with the same observed successful outputs. In one, the system already possesses a deployable equivalent of c and selects it now. In the other, it constructs the relevant bindings during this episode. Unless the observations or additional provenance exclude one history, the success record is compatible with both New and not-New. Therefore that record alone does not entail New.

This is an underdetermination result for this evidence, not a theorem that newness can never be established. Complete relevant provenance, an inspectable bounded repertoire and a justified equivalence relation could change the premises. Unknown pretraining is a concrete unresolved dependency in the present model-wide attribution.

The DSL adds another explicit premise: its interpreter and available operations are supplied organization. Successful composition may still involve construction, but success does not show that the operator supplied no load-bearing structure. New relative to a recorded initial operative program is a narrower claim than New relative to the whole pretrained system.

## P6. Finite repair with protected behavior is directly testable

Fix finite obligation families O and P, an interpreter, input domain and background. Let a recorded change Delta replace the actual operative program p with p'. Suppose a named o in O fails for p and passes for p'; every r in P that passes for p also passes for p'; and execution receipts establish that Delta installed p' and the tested behavior was produced through that change.

Under the interpretation and provenance premises, these observations satisfy the finite instance of Repair O,P in ECS §9.1. The proof checks its conjuncts: an obligation changes from failed to satisfied, protected successes remain, and the named change produces the alteration. For finite exhaustively evaluated O and P, there is no untested member of those particular families.

The conclusion is exactly that repair contract. It does not imply preservation of unlisted behavior, the correctness of the interpreter, explanatory bearing, New, or CreateEK. If a revision fixes an expiry example while breaking replay, and replay belongs to P, it fails this repair claim. If an unsound checker calls the revision successful, §5.4 requires criticism of the candidate-plus-auxiliaries-plus-interpretation conjunction.

An unchanged task already solved by p cannot witness a newly repaired obligation in this contract. That is why a saturated initial task needs a new informative condition, rather than a favorable narrative about unchanged passes.

## Feasible next control: fixed-prefix final-request replay

After a preregistered Mini run closes, copy its final revision call's exact public request payload into a plain API caller that does not load Mini's graph, manifest or runner. Preserve all messages, model, thinking setting, response format and completion allowance. Record the new request hash and confirm equality with the original payload hash. Give the plain caller the same frozen public prefix, including the criticism and observations already embedded in it. Score its new answer with the same final verifier. Use several interleaved repetitions if estimating variability is worthwhile.

This is a conditional endpoint control: does invocation through Mini have any additional effect once its entire effective request is supplied? P2 predicts the same conditional law, subject to provider-state stability. It does not compare equal end-to-end costs, because the copied prefix contains work previously done by Mini. It does not show that the critic was unnecessary, because its content remains in the supplied request. It does not test the adaptive controller as a whole.

For an end-to-end machinery control, implement a plain serialized workflow that creates its own proposal, runs the same public checker, asks its own critic and revision with the same rendering policy and ceilings. That control tests whether Mini contributes beyond implementing that policy. Removing only the critic text from a matched revision request is a different intervention; retain raw observations and task information so criticism carriage is isolated. Removing both would test a combined feedback intervention.

## What remains empirical

| Question | Required evidence beyond these deductions |
|---|---|
| Does a candidate template help? | Valid matched runs, concrete failure diagnoses and fresh task conditions |
| Does criticism guide the repair? | Content-controlled contrasts and a logged operative path |
| Does Mini add to the corresponding prompt policy? | The end-to-end serialized-policy comparison, with matching information and resources |
| Is an output an explanation? | A defensible interpretation and independent assessment of the ECS accounting clauses |
| Was a creative contribution made? | The remaining Attempt, New, Build, episode and attribution evidence |
| Is ECS's constitutive conjecture correct? | Independent counterexample arguments under fixed grains; application scores alone are insufficient |

These propositions constrain what may be inferred. The campaign supplies the empirical answers, including failures of the proposed mappings and conditions under which no conclusion is available.
