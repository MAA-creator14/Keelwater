# A2 rewrite (AI draft, for review)

Drafted by the AI from its review of the original A2. **Thresholds in brackets are proposals. The human sets them at the Stage 3 gate, before any test runs.** Sample sizes are invented.

## A2: wrong payouts come from handlers overlooking information in the claim

| Field | Draft |
|---|---|
| Assumption | When a claim is paid wrongly, it's mostly because the information that would have changed the decision was in the claim when it was sorted, and the handler didn't use it. Examples are a linked or earlier claim, or a policy rule. |
| Type | Problem |
| Why it's here | The Stage 1 problem is about time, not accuracy. But any change to sorting (bulk sorting now, suggestions later) must not raise wrong pay. This assumption decides whether showing more context at sorting is the right fix (Failure 4, missing context). |
| Risk if wrong | We build ways to show claim context at sorting, but the wrong payouts actually come from data that is missing or arrives late (Failure 5), or from unclear policy rules. Wrong pay doesn't fall. |
| Cheapest test | Take 30 past wrong payouts from reversal, recovery or complaint records. The 3.4% figure is pile moves, not wrong payouts, so it isn't a source. Mix in 30 correctly paid claims. Two experienced handlers review all 60 without knowing which are which. For each claim they say whether information that would have changed the decision was in the claim when it was sorted. |
| Validity check | If reviewers flag "overlooked information" on correct claims at a similar rate to wrong ones, the result is hindsight noise, not evidence. |
| Pass threshold | [proposed: in 30% or more of wrong payouts, both reviewers agree the deciding information was in the claim at the time, and the rate on correct claims is clearly lower] |
| Fail threshold | [proposed: 10% or less of wrong payouts meet that bar] |
| Between pass and fail | Break the results down by type of information (linked claims, earlier claims, policy rules). Act only on a type that recurs. |
| What changes if wrong | Fix the data instead: capture missing information at intake, and clarify policy guidance on the suspicious pile (T28). Don't build context display. |
| Depends on | Being able to find 30 wrong payouts in reversal, recovery or complaint records. If they can't be found, the test needs a different source. |
