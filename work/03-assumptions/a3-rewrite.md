# A3 rewrite (AI draft, for review)

Drafted by the AI from its review of the original A3. The original was split into two assumptions: accuracy (A3a) and value (A3b). **Thresholds in brackets are proposals. The human sets them at the Stage 3 gate, before any test runs.** The 80-claim set is invented.

## A3a: accuracy

| Field | Draft |
|---|---|
| Assumption | AI-suggested sorting makes no more dangerous errors than handlers do today. A dangerous error is a claim wrongly sorted as "simple", which is the wrong-pay case in Failure 1. |
| Type | Accuracy |
| Risk if wrong | Claims that need investigation are paid. Money goes out wrongly, the insurer can't defend the decision to the regulator, and handlers stop trusting the tool. |
| Cheapest test | Stage 4a system test. Run the three variants (rules baseline, the old predictive prototype and an LLM classifier) on the 80 invented claims, stratified with hard cases over-sampled. Compare against labels checked by a senior handler, not raw handler labels. Report wrong-"simple" overall and on the linked-claim subset separately. Experienced handlers and compliance review the riskiest decisions blind, without knowing which variant made them. Results are labelled as a simulation on a small sample. |
| Pass threshold | [proposed: wrong-"simple" rate at or below the senior-handler-checked handler rate overall, and zero on the linked-claim subset] |
| Fail threshold | [proposed: any wrong-"simple" on the linked-claim subset, or an overall rate above the handler rate] |
| What changes if wrong | AI may only route claims toward a human (closer look or suspicious). It never clears a claim for payment. If it can't meet even that, stop. |
| Depends on | The label audit of the 3.4% reclassification measure with a senior handler. Without it, there's no reliable reference to compare against. |

## A3b: value

| Field | Draft |
|---|---|
| Assumption | AI suggestions cut handler time per sorting decision without adding work elsewhere, such as more overrides or more escalations. |
| Type | Value |
| Risk if wrong | We build it and save no time. Or it sends more claims to closer look or suspicious, which clogs investigation (Failure 2, T19, T28). |
| Cheapest test | Stage 4b simulated suggestion screen. Measure time to decision with and without a suggestion, the override rate, and the share sent to suspicious against the baseline. Results are labelled as a simulation on a small sample. |
| Pass threshold | [proposed: median time to decision down by at least _% with a suggestion, and the share sent to suspicious no higher than without] |
| Fail threshold | [proposed: no reduction in time to decision, or the share sent to suspicious goes up] |
| What changes if wrong | Drop AI suggestions. Keep bulk sorting, and put effort into the information and approval flow (A1). |
| Note | If A1 holds, A3b matters less for the long waits. The 11-minute median is already fast, and the four-hour waits come from waiting, not from deciding. |
