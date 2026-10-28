# Stage 5 assumptions (invented)

Set by the human on 28 Oct 2026 from the AI's proposed ranges. Used by `compare_options.py`.

## Batch filter B

A claim goes into the bulk batch if all of these hold: policy number present, all required documents received, no claims in the last 12 months, no related claims recorded, policy over 60 days old, amount under £1,000. On the 80 claims this batches 27, of which 1 needs a closer look (K075).

## Bulk sorting

| Assumption | Low risk | Middle | High risk |
|---|---|---|---|
| Seconds to scan one claim in a batch | 5 | 10 | 20 |
| Seconds of overhead per batch (set up and confirm) | 30 | 60 | 120 |
| Chance the handler spots a non-simple claim and pulls it out | 80% | 50% | 20% |
| Chance the handler pulls out a simple claim unnecessarily | 2% | 5% | 10% |

- A pulled-out claim is reviewed individually, at the status-quo time per claim.
- A non-simple claim that's pulled out has been spotted, so it goes to its correct pile. A simple claim pulled out unnecessarily is sorted by the simulated handler.
- Claims outside the batch are sorted as in the status quo.
- Results are expected values, not random draws.

## Status quo

- Piles: the simulated handler piles from Stage 4a (invented).
- Time per claim: the human's median from the 4b pilot without a suggestion (36 s, 12 claims, one person, on the mock screen, not Keelwater's real screen).

## Known effect of the model

Inside the batch, simple claims are sorted simple unless pulled out, so the simulated handler's invented errors on those claims don't carry over. That lifts bulk sorting's accuracy against the status quo for reasons that come from the simulated baseline, not from anything observed.
