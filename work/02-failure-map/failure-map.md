# Stage 2 failure map

Where the output can be wrong, ranked with wrong-pay first. Failures 1 to 3 are my draft. Failures 4 to 6 were added at review, from the AI's list of missing modes; I chose which to keep. The steps were also added at review.

Steps: intake → sorting → reason → handler review → payment → later reclassification.

Ticket and account references (T, D, A) point to the invented sources in `work/01-signals/`.

| # | Failure | Step | Scenario | Test | Guardrail |
|---|---|---|---|---|---|
| 1 | Wrong payout decision | Sorting → payment | A complex claim that requires investigation gets sorted into the "simple" pile. | Test high-risk or ambiguous claims. | No automatic payment for claims sorted automatically, unless necessary controls or approvals have been met. |
| 2 | Sorting into the wrong pile (no money out) | Sorting | A simple claim is sorted into the needs a closer look or suspicious pile unnecessarily. | Compare LLM-predicted sorting against sorting by handlers, on the same sample. | |
| 3 | Missing or incorrect explanation | Reason | The suggested pile is correct, but its explanation mentions information that isn't in the claim, or doesn't cite the reason or policy why a claim needs investigation. | Experienced handlers and compliance staff independently assess the evidence supporting each reason, including whether it's sufficient for a customer or regulator. | |
| 4 | Missing context | Intake | Linked, duplicate or earlier claims aren't seen, for example a claimant who has had an accident before (T06, T21, T34). | Wrong-pay on the linked and duplicate subset, reported separately from the overall rate. | |
| 5 | Stale or partial inputs | Intake → sorting | A claim is sorted before the missing information arrives, then moved later (T12, T13). | Sort on partial records, then compare against the same claims once complete. | |
| 6 | Handler over-trust | Handler review | Handlers accept wrong suggestions, or make errors when bulk sorting at speed. | Rate of wrong suggestions accepted, and errors per bulk action. | |

## Decided at review

- Failure 2 narrowed to wrong-pile errors where no money goes out. Failure 1 owns every wrong-pay case.
- Drift (the claim mix changes, so accuracy drops over time) was offered and not kept.

## Open

- Failure 1: "high-risk or ambiguous claims" and "necessary controls or approvals" are not yet defined.
- Failure 2: handlers' sorting is noisy as a reference (3.4% moved within 30 days, T05). The test covers only the LLM variant, and doesn't check whether confidence tracks accuracy.
- Failure 3: needs a scoring scale. Stage 4a sets a five-point rubric.
