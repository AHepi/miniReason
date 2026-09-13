# FCL-1: a fallible commitment language proposition

Root proposition, REC-20260914-B. Prospective H005 candidate; no empirical advantage claimed.

## Conjecture and intended use

**FCL-1 (Fallible Commitment Links)** may help a small model return to a mistaken assumption after several complete template invocations because it makes a proposed use, its dependencies, a criticism and a later response separately addressable. Its intended use is an extended prose inquiry in which the problem, the criticism and the relevant commitments may change.

This is a proposed combination of familiar reference, dependency and criticism devices, not a claim of a historically new formal language. The hypothesis concerns actual use across cycles. Mere well-formed output, more references, more criticism or longer retention would not establish an advantage.

## Carrier and grammar

Every model contribution has two independently authored strings: `body` and `commitments`. The body is unrestricted public prose. FCL-1 uses the following JSON document, encoded inside the commitments string:

```text
Document := {"language":"FCL-1", "records":[Record*], "uptake":[Ref*]}
Record := {"id":LocalName, "type":Type, "text":Prose, optional fields}
Type := "claim" | "commitment" | "objection" | "use" | "problem"
Ref := LocalName | QualifiedName
QualifiedName := <exposed artifact label> "#" LocalName
optional fields :=
  "scope":Prose, "action":Prose, "consequence":Prose,
  "grounds":Prose, "bearing":Prose,
  "target":[Ref*], "depends":[Ref*], "mentions":[Ref*],
  "revises":[Ref*], "withdraws":[Ref*]
```

Local names are unique within an authored document. Prose is any JSON string. References identify authored content, never hidden reasoning. Empty records or uptake are permitted. Missing context, uncertain references and inability to express a relation can be said in prose; no slot must be filled with an invented claim. Malformed documents are retained as opaque contributions and remain available for later criticism. The harness does not repair a document by inventing semantic content.

## Interpretation

- A **claim** makes a proposition discussable without conferring standing.
- A **commitment** proposes what taking some content up involves in a stated scope: an application, action, implication or consequence. Its author may give a ground or proposed way it could be challenged. The test's relevance and the commitment itself are fallible.
- An **objection** alleges a defect at a target and may state grounds and their bearing. It need not be valid to be a criticism or to be used.
- A **use** records an author's proposed uptake or response. `revises` and `withdraws` assert a change; they do not prove it happened in later work.
- A **problem** states an unresolved or newly encountered question, without requiring it to be solved or scored.
- `depends` asserts that this proposed use relies on the referenced content. `mentions` only locates material. Neither is automatically inferred from citation or lexical overlap.
- `uptake` identifies the records the author currently proposes to use. It is a local claim about standing, not a harness verdict or a truth label.

An example of form, excluded from participant requests, is a commitment to use a household arrangement under an assumed availability and an objection showing that availability was misread. Neither that example nor any expected repair is seeded into the daily problem.

## Three-cycle proposition

A first template constructs and criticizes an account and issues body plus commitments. A second complete template can expose selected earlier commitment surfaces, question their grounds and return its consequences to the account. A third complete template can revisit an older criticism or method as well as the current account. These are complete invocations containing multiple model calls, not three responses renamed as cycles.

Different problems may need different connectivity. The language does not prescribe one topology, an order of record types, a required error, a universal repair procedure or a compulsory layout for the body. Original artifacts persist in the evidence store while each node sees only its declared views.

## Comparisons and possible defeat

Compare FCL-1 Mini with a Mini free-prose commitment surface under the same topology and resource settings. The prose condition receives the same meaning of commitment, dependency versus mention, and fallible criticism, expressed as permission to write ordinary prose. This controls for adding those ideas rather than their formal notation.

Compare both with matched multi-call prose outside Mini and with bare and native-reasoning public-answer chains. Five arms can execute concurrently subject to actual dependency readiness and one global five-request limit. Native hidden reasoning is neither retained nor passed on.

The proposition can fail through unusable encoding, displaced useful prose, false dependency claims, loss of relevant context, criticism that never changes use, or repairs also achieved by the controls. Such outcomes remain evidence. Root will argue from particular error-correction episodes, including corrections of prior criticisms and losses caused by the carrier. No score, answer key or automatic semantic admission test will determine the conclusion.

The research can establish a candidate use case, a limitation or an unfavorable comparison. It cannot promise superiority before observing the work or establish general recursive closure in three to five cycles.
