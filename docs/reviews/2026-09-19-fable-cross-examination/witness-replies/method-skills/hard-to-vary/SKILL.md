---
name: hard-to-vary
description: Tests whether an explanation is "hard to vary" (David Deutsch's mark of a good explanation) - whether every part does real work, so that changing any part would break its power to explain. Use this whenever someone gives or asks for a reason WHY something happened, works, failed or should be done and wants to know if the reasoning holds up - a theory, diagnosis, root cause, post-mortem, bug hunt, business or history explanation, design or plan rationale, argument, proof, rule, or a creative choice such as why a scene or detail is there. Trigger on "does this hold up", "stress-test my thinking", "is this a just-so story", "is this circular", "are we fooling ourselves", "is this detail doing any work", "is this a good explanation", and any mention of "hard to vary" or Deutsch. Also use it quietly on your own explanations when the stakes are high. Not for looking up facts, matters of pure taste, or judging how accurate a forecast was.
---

# Hard to vary

A good explanation is hard to vary: you cannot change its parts and still have it explain what it is meant to explain. A bad explanation is easy to vary: its details could be swapped for others and it would "explain" just as well, which shows the details were never held in place by the thing being explained.

The idea is David Deutsch's (*The Beginning of Infinity*). This skill sharpens it using a formal theory supplied by the user, "Claude Fable Semantics". That theory's terms are mapped to plain words in `references/word-list.md`.

This skill is a way of criticising, not a truth-meter. Passing does not prove an explanation true. Failing does not prove it false. It shows which parts are held in place, which are loose, and what would tighten them.

## The idea in one example

Why are there seasons?

*Old story:* a goddess grieves for part of each year, and her grief makes winter. Swap the goddess for another. Change why she grieves. Change the bargain that sets the dates. The story works exactly as well every time. Nothing about winter holds any detail in place. Now add one more job: when it is winter in the north it is summer in the south. The story breaks, because grief would chill the whole world at once.

*Tilt:* the earth's axis leans, so each half of the world gets more direct sun for half the year. Remove the lean: no seasons. Change the angle: stronger or weaker seasons. Flip which half leans towards the sun: the seasons swap. The extra job, opposite seasons in the south, is done with no change at all. Every part is held in place by something you could check.

## Three things that can change. Keep them apart.

Most muddle comes from mixing these up.

1. **The parts of the explanation.** Remove one, swap one, add one, rewire them. This is the "varying" in "hard to vary".
2. **The world.** The changes to the situation that the explanation claims to cover: poke this, remove that, run it somewhere else. This skill calls it the **change list**. An explanation is tested by whether it keeps matching the world as these changes are made. A story that only fits one fixed outcome has not been tested at all.
3. **The question.** What is being explained, over what range, and what exactly is asked. This must be **frozen** during a test. It may be changed afterwards, but that makes a new claim, and must be written down as one.

So: an explanation is hard to vary when few changes of kind 1 survive, where "survive" means it still matches the world under every change of kind 2, for every job it has, with kind 3 held still.

## The stance

- **Loose is not wrong.** A loose part may be true. It is just not held in place by anything yet. The aim is to find what would hold it.
- **Judge against the question asked.** An explanation can be tight for one question and idle for another.
- **No scores.** Do not count confirmations, jobs or parts. One job that rules out rivals is worth more than ten that rule out nothing.
- **Not on the list of tests:** short, simple, elegant, popular, said by an expert. None of these holds a part in place.
- **Some things are allowed to be loose.** Names, conventions, tastes and free design choices can be otherwise. Say so plainly, and do not dress them as explained.
- **Plain words, concrete verbs.** Remove, swap, flip, reverse, poke, add. Show the case before the general point.

## The procedure

Read `references/the-idea-in-depth.md` before a first full run in a conversation. It gives the reason behind every step.

**Step 1 - Freeze the question.** First make sure there is something to explain: "sales dropped" compared with what? A thing that did not happen needs no explanation, and explaining it anyway is the easiest way to build a loose story. Then say what is being explained, over what range, and what is asked. Name the kind of question, because the tests differ:
- *What produces it?* (forward, from causes)
- *What can we tell from what we see?* (backward, from evidence)
- *Why can it not happen?* (something blocks every route)
- *Why is there none of it?* (something is absent)
- *What counts as what under this rule?*
- *Does it achieve its purpose?*

**Step 2 - List the jobs.** The particular things the explanation has to account for, each put as a contrast: why this *and not that*.

**Step 3 - Take it apart.** List the parts that are claimed to do the work. Use the owner's own words. Say it back and ask, "Is this a fair version?" Test the strongest version, not a weak one.

**Step 4 - Write the change list.** Which changes to the world does the claim cover? Which does it leave out, and was that said up front or slipped in later? A list with nothing on it that could have mattered is an empty test.

**Step 5 - Run the tests.** Full wording is in `references/question-bank.md`.
- **Remove** each part. Does it still do every job? Then try removing parts in pairs and groups.
- **Swap** each part for a near neighbour. If the swap works as well, the part is loose. If not, name what stops it: that is what holds the part in place.
- **Flip the outcome.** Had the opposite happened, could the same explanation have covered it? If yes, it explains nothing.
- **Poke.** For each part, name one change to the world that should alter the outcome, and one that should not. A part with no such pair is a label, not a working part.
- **Reverse.** Is it running backwards from the result? Poke the supposed cause and see if the effect moves; poke the effect and see that the cause does not.
- **Hunt the answer in the starting points.** Is the conclusion already sitting there under another name: "nature", "law", "tendency", "that kind of thing"?
- **Add a job.** Find something else that must also be so if the explanation is right. Does it survive unchanged? Did the new job rule out any rival version? If not, it added nothing.
- **Build the best rival.** Find a change that tells the two apart. If no change on the list can, they are the same explanation at this level. Say so, or ask a finer question and record it as new.
- **Check the patches.** When it failed before, how was it rescued? A patch that narrows the claim quietly, or adds a part with no other job, makes it easier to vary.
- **Look inside.** Matching the results is not matching the workings. Two machines can give the same outputs by different routes. To test an explanation of the workings, use changes that reach inside.

**Step 6 - Ask where each part came from.**
- *Fitted:* tuned on past cases. It is held in place only on the kinds of change it has met. Ask what it has never met.
- *Built:* worked out with the thing itself in view, and criticised. It says something definite about unmet changes, so it can be caught out.
- *Asserted:* someone simply said so.

**Step 7 - Report.** See below.

## The quick version

For a small claim, three questions are enough.

1. What exactly is this explaining, and what would we see if it were wrong?
2. Take its most colourful detail and swap it. Does it still work?
3. Flip the outcome. Could it have explained the opposite just as well?

## How to ask

The way a question is put decides whether you get a test or a story.

- **Ask for the change, not the justification.** "Why do you believe that?" invites a story. "What happens to your explanation if we take this part out?" invites a test.
- **One part and one change at a time.**
- **Hand them the tool.** "Give me a different version of this detail that would work just as well." If they can, the part is loose. If they cannot, ask what stops them.
- **Always ask for both halves of a poke:** a change that should matter and one that should not.
- **When the answer is a label** ("it's the culture", "it's the algorithm"), ask: "What would be different, and where would we see it, if that were not so?"
- **When a patch appears,** ask: "Is that the same claim as before, or a new one? What else does the new part have to account for?"
- **When facts are missing, do not guess.** Turn the gap into a poke that could be run: "If we showed the old page to half the visitors now, what does your explanation say would happen?"
- **Keep the tone of a fellow mechanic,** not a prosecutor. You are looking for the loose bolts so they can be tightened.
- **Stop** when every part is marked as held (and by what), loose (and what could replace it), idle (removable), borrowed (held in place by some other explanation that is not being tested here; name it), or unknown (and what test would settle it).

## The report

Keep it in proportion. For a full run:

1. **The question, frozen.** What, over what range, what is asked.
2. **The explanation in parts.**
3. **Part by part:** held in place (by which job or change), loose (what could replace it), idle (can be removed), borrowed (rests on another explanation; name it), or unknown (what would settle it). A table is fine.
4. **Whole-explanation checks:** flip, direction, answer hidden in the starting points, what the change list leaves out, rivals, and where the parts came from.
5. **What would make it harder to vary:** the one or two jobs, pokes or cuts that would tighten it most.
6. **What this does not show.** Hard to vary is not the same as true.
7. **One next step.**

## Reference files

- `references/the-idea-in-depth.md` - what "hard to vary" means in full, with the reason for each step. Read before a first full run.
- `references/question-bank.md` - the exact wording for each test, the follow-ups to common dodges, and how to question yourself.
- `references/by-domain.md` - what the tests look like for diagnoses, designs and plans, arguments, history, stories, proofs, rules and written instructions, each with a small case.
- `references/word-list.md` - plain words matched to the terms of the source theory, and where that theory is kept.

## Traps

- **Using it as a truth-meter.** It finds loose parts. It does not certify anything.
- **Letting the question drift mid-test.** Freeze it. If it must change, write down that it changed.
- **Testing only against a fixed outcome.** With nothing on the change list, any story passes.
- **Counting.** More confirmations of the same kind hold nothing new in place.
- **Mistaking a label for a part.** If no change to the world could tell the label from a different one, it does no work.
- **Calling a part idle too soon.** Two parts may each be removable alone but not together. Remove in groups before you cut.
- **Assuming more detail is harmless.** An added part can break an explanation that worked without it.
- **Demanding tightness from things that are free.** Conventions and tastes may be loose. Only the claim that they are *explained* needs testing.
- **Prosecuting.** People defend stories when attacked and test them when invited.
- **Copying the books.** Use Deutsch's idea in your own words. Do not paste passages from his work.
