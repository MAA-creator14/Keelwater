# Stage 4b pilot results

**One-person pilot on 24 invented claims (12 with an AI suggestion, 12 without). A simulation with a very small sample, not evidence about real handlers.** See `test-notes.md`.

| Measure | With suggestion | Without |
|---|---|---|
| Median time to decision | 61 s | 36 s |
| Correct pile (against the policy labels) | 58% | 83% |
| Wrong-simple decisions | 1 ['K035'] | 0 [] |
| Escalated (suspicious, or escalate ticked) | 8% | 8% |
| Requested missing information | 42% | 25% |

**Handler time saved with a suggestion: -71%** (median, with against without).

## Trust in the AI suggestion

- Overrides: 6 of 12.
- Wrong AI suggestions accepted: 1 of 3 ['K035']
- Correct AI suggestions overridden: 4 of 9 ['K063', 'K002', 'K010', 'K007']

## A3b (thresholds locked at Stage 3)

Pass: 30% or more of handler time saved, with override, reclassification and escalation rates no higher than without. Fail: 10% or less saved, or any of those rates higher.

- Time saved: -71%
- Escalations: 8% with, 8% without
- Overrides: can only happen with a suggestion, so there is no "without" rate to compare. Reported above, not tested.
- Reclassifications: happen up to 30 days later, so they can't be measured in a pilot. Not tested.

**Verdict on what could be tested: fail.**
