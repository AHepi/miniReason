# By domain

This file shows what the tests look like in different kinds of work. The method is the same everywhere. What changes is what counts as a part, a job, and a change to the world. Each section gives those three, the tests that bite hardest, and a small case.

Contents: 1 Diagnoses and root causes. 2 Designs and plans. 3 Arguments. 4 History and one-off events. 5 Stories and other creative choices. 6 Proofs and mathematics. 7 Rules and definitions. 8 Written instructions. 9 Traps.

---

## 1. Diagnoses and root causes

*Bugs, outages, illnesses, "why did sales drop", post-mortems.*

- **Parts:** the suspected fault and each link from it to the symptom.
- **Jobs:** every symptom, *and* every place the symptom did not show.
- **Changes to the world:** put the fault back and take it away; run the same thing where the fault is absent.

**Tests that bite:** flip; reverse; add a job; look inside.

**Case.** "Sales dropped in March because of the website redesign."
- *Add a job:* did sales drop for people who never visit the site (phone orders, the other region)? If they dropped there too, the redesign cannot be doing that job.
- *Flip:* had sales risen, would the redesign have got the credit? Then it explains both.
- *Poke:* show the old site to half the visitors now. The explanation says their sales recover. It also says changing the price should *not* matter. Both halves can be tried.
- *Reverse:* were sales already sliding, and the redesign launched *because* of that?

The "did not show" jobs are the ones people forget. A diagnosis that accounts for every broken machine and none of the working ones is half tested.

---

## 2. Designs and plans

*Why this architecture, this process, this route.*

- **Parts:** each design decision.
- **Jobs:** each requirement the design must meet.
- **Changes to the world:** the loads, failures, growth and misuse it must stand up to.

**Tests that bite:** remove; swap; check the patches.

Every decision gets one of three honest marks: **held** (name the requirement that forces it), **free** (any of several would do; say so, and pick for convenience), or **inherited** (there because it was there before). Trouble comes from free and inherited choices presented as forced.

**Case.** "We need a message queue between the two services."
- *Remove:* call directly. Which requirement fails? If the answer is "when the second service is down, orders are lost", that requirement holds the queue in place. If the answer is "it's best practice", nothing does.
- *Swap:* a plain database table polled every second. Does every requirement still pass? Then "queue" is loose and "something that holds orders while the other side is down" is the held part.

Swapping often shows that the held part is more general than the one named. That is a finding, not a failure.

---

## 3. Arguments

*A case for a conclusion.*

- **Parts:** the starting points and each step.
- **Jobs:** to make the conclusion follow, and to not equally support its opposite.
- **Changes to the world:** different cases to which the same reasoning would apply.

**Tests that bite:** hunt the answer in the starting points; flip; swap the subject.

**Case.** "This policy is good because it's what people want, and we know they want it because they'd choose what's good."
- *Hunt:* each starting point needs the conclusion to stand. It goes in a circle.
- *Swap the subject:* run the same steps for a policy everyone agrees is bad. If the steps go through just as well, they are not what is holding the conclusion up.

Remember: taking away a reason removes the support. It does not show the conclusion is false.

---

## 4. History and one-off events

*Why the war started, why the company failed.*

Here nobody can step in and change things, so the change list is made of **comparisons**: other times and places where a part was present or absent.

- **Parts:** each named cause.
- **Jobs:** why then, why there, why that way, and why *not* in the similar cases where it did not happen.
- **Changes to the world:** the differences between this case and its nearest neighbours.

**Tests that bite:** add a job; flip; build the best rival.

**Case.** "The company failed because its founder was arrogant."
- *Flip:* had it succeeded, would the same trait be called boldness? Then the label does no work.
- *Add a job:* what about the equally arrogant founders of firms that thrived? The explanation must say what was different.
- *Rival:* "it ran out of cash before the product was ready." What would tell the two apart? Look for a decision where arrogance and cash pull in different directions.

Be plain that parts here are held less tightly than in a laboratory, and say which comparisons are doing the holding.

---

## 5. Stories and other creative choices

*Why this scene, this image, this detail.*

This does not test whether a choice is beautiful. It tests the claim that a choice *does certain jobs*.

- **Parts:** the choices: place, action, object, order, who knows what.
- **Jobs:** what each choice is said to do: set up a later payoff, show a flaw, contrast with another scene, leave the audience with a particular question.
- **Changes to the world:** changes elsewhere in the story. Move the scene, cut the payoff, change who is present.

**Tests that bite:** remove; swap; two routes to one job.

**Case.** A rescue story opens with the hero climbing a lift shaft by hand. Later the lift falls down that shaft and she saves herself by catching a ledge.
- *Remove the climb:* the fall has nothing to contrast with; the catch is luck.
- *Swap it for climbing stairs:* slow, effortful, upward, so the contrast job is still done. But she never touches the ledge, so the catch is no longer earned. The job "earn the catch" is what holds *this shaft* in place.
- *Swap "fifty-one rungs" for forty:* nothing changes. The number is free. What is held is that she had *counted* them.
- *Two routes:* she hides a chipped tooth and she hides a warning tag. Both show that she conceals harm. Either alone would do. Keep both only if each has a second job.

A scene that survives every swap is decoration. A scene that does four jobs at once is very hard to replace, and that is what people mean when they say a story feels inevitable.

---

## 6. Proofs and mathematics

Nothing here can be poked in the physical sense. The changes are changes to the **conditions**: drop one, weaken one, change a dimension.

- **Parts:** each condition of the statement and each step of the proof.
- **Jobs:** the conclusion, and its failure when a condition is dropped.
- **Changes:** remove each condition in turn; remove them together.

**Test that bites:** remove, with a counter-case.

**Case.** "Every square table of numbers with an odd number of rows that is its own negative when flipped across the diagonal has no inverse."
- *Drop "own negative when flipped":* the plain 3-by-3 identity table has an inverse. So that condition does work.
- *Drop "odd":* a 2-by-2 table of that kind has an inverse. So that one does work too.

For each condition, show a case that gets through when it is dropped. If you cannot, the condition may be idle and the result may be more general than stated. A shorter proof is pleasanter. It is not better held.

---

## 7. Rules and definitions

*What counts as what.*

A rule is told from a cause by what it responds to. Change the world and a rule's verdict on a given case stays the same; rewrite the rule and the verdict changes. A cause is the other way round.

- **Parts:** the clauses.
- **Jobs:** sorting the clear cases the right way, and giving an answer on the hard ones.
- **Changes:** edits to each clause.

**Test that bites:** remove each clause and ask which cases change sides.

Keep three questions apart, because an answer to one is not an answer to the others: *What does the rule say about this case? Do people in fact follow it? Should it be the rule?*

---

## 8. Written instructions

*Prompts, checklists, procedures.*

- **Parts:** each instruction.
- **Jobs:** each behaviour the instructions are meant to produce or prevent.
- **Changes to the world:** the different inputs and situations the reader will face.

**Tests that bite:** remove; swap; look for parts that fight.

For each line ask: if this were deleted, what would the reader do differently, and in which situation? A line for which the answer is "nothing" is idle. Also look for a line that breaks what another line achieves. Instructions that say *why* are harder to vary than bare orders, because the reason tells the reader what to do in the situations nobody listed.

---

## 9. Traps

- Forgetting the "did not happen" jobs in a diagnosis.
- Calling a design choice forced when it is only familiar.
- Treating the loss of an argument as the loss of its conclusion.
- Pretending that comparisons in history hold parts as tightly as experiments do.
- Using this test to rule on taste. It can only test the claim that a choice does a job.
- Cutting both of two routes to one job because each looked removable alone.
