# Stage 5 draft: options and decision (human draft)

Fill in each section. Short answers are fine. The AI reviews this, then builds the comparison.

## Evidence so far (for reference)

All from simulations on 80 invented claims. Correct piles follow the human's sorting policy.

| Option | Evidence | Key result |
|---|---|---|
| Status quo | 4a simulated handler baseline; 4b pilot without suggestion | 85% accuracy, 7.5% wrong-simple (simulated); 36 s median decision (one person, 12 claims) |
| Bulk sorting | None yet. Squad halfway through building it; ships in about six weeks | — |
| Suggested sorting, human decides | 4a LLM; 4b pilot with suggestion | LLM 17.5% wrong-simple alone; with suggestion 61 s median, 58% accuracy, 1 of 3 wrong suggestions accepted (one person, 12 claims) |
| Auto-clear of simple claims | 4a, all variants | All fail A3a. Ruled out at the 4a gate (AI may only route toward a human) |

Not yet tested: A1 (are the four-hour waits information and approval waits, not the queue?). It needs real claim timelines.

## 1. How to simulate the untested options on the same 80 claims

- Status quo (what you'd use: the simulated handler piles, your 4b timings, anything else): Use the existing simulated handler decisions and my Stage 4b timings. If timings only cover 12 claims, don't extrapolate them as if all 80 were observed.
- Bulk sorting (which claims a handler could sort in one batch, how much faster per claim, how often a handler errs when sorting at pace): Define which claims can be grouped into a batch, run the existing rules or other approved sorting logic across them, and estimate the time to review a batch using (measured per-claim and batch-level timings). Include time to resolve exceptions and correct errors.

## 2. Measures (from SKILL.md)

For each, say how you'd measure or estimate it, or mark it "not measurable in this simulation".

- Efficiency (handler minutes): Total handler minutes for the set of 80 claims (incl. batch creation, overrides, etc). Use actual observed timings where possible.
- Data output (what each option records, for example reasons): Pile, reason, cited facts and policies, linked claims, missing data, override and final decision. Make sure that explanations have supporting evidence.
- Speed to payment, median and 90th percentile: Median and 90th-percentile time from claim arrival to actual payment. Not measurable in this simulation since it only covers sorting.
- Guardrails (overrides, escalations, reversals, handler error under pace): Wrong-simple rate, per-pile confusion matrix, overrides, escalations, reversals and handler errors under time pressure.

## 3. What you expect

- Which option you expect the evidence to support, and how confident you are: I expect the evidence to support the bulk sorting, as my assumption is that this is will speed up the sorting whilst retaining accuracy of sorting decisions.
- What would surprise you: if either the status quo or the bulk sorting perform worse compared to the AI generated suggestions, in terms of wrong simple count, accuracy, etc.

## 4. For the gate (you decide these after seeing the comparison)

- Option to take forward: not decided yet until bulk sorting has been compared on the same claims and guardrails against the other options.
- Gate weight for each later stage (light, standard or formal): standard
- What would make you reverse the decision: evidence that another option improves handler time and decision quality without increasing dangerous errors; evidence that lengthy queues are caused by other factors
