# AIPDLC log: keelwater-sorting

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 1, Frame the signal
**Proposed:** Problem framing: the slow tail, not the average, is the problem to solve.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Written after reviewing AI suggestions on 26 Oct. Own view: the median of 11 minutes is already fast, so the problem is the long tail (15% over four hours). Confidence in the 15% figure is high because it is in the brief; confidence in its cause is low. Adopted from AI: none. Not yet tested: whether the tail is a sorting problem.

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 2, Failure map
**Proposed:** Two expected failure families: wrong pile on claims that look simple, and right pile with the wrong reason.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Written after reviewing AI suggestions on 26 Oct. Own: the "claimant has had an accident before" case, a concrete example of the first family. Adopted from AI: the two-family structure and the wrong-reason example. Still to add: which of these handlers would recognise first.

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 3, Evidence and assumptions
**Proposed:** Riskiest assumption: the four-hour wait is caused by information or approval waits, not by the queue.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Written after reviewing AI suggestions on 26 Oct. Own: the assumption itself and why it is the riskiest, because if it is true, sorting automation does not help the tail. Adopted from AI: the 60-claim sample, the four time categories, and the 30% and 15% thresholds. Own change to make before the test: sample from the last 12 months only if the data is clean enough to classify time spent.

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 4a, System test
**Proposed:** Rules-based variant expected to have the lowest wrong-pay rate; LLM classifier expected to miss linked-claim context.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Rewritten after reviewing AI suggestions on 26 Oct. Own: the rules variant will be more cautious and raise more false positives for handlers. Adopted from AI: the expectation that the LLM misses linked claims, and the linked-claim subset as the test. Check that would prove this wrong: wrong-pay on the linked-claim subset, reported separately from the overall rate.

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 4b, UI mock
**Proposed:** Handlers will not immediately trust automated suggestions; the UI needs to make override easy.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Rewritten after reviewing AI suggestions on 26 Oct. Own assumption: handlers will not trust suggestions by default. Adopted from AI: the override-as-trust-mechanism idea. To test: override rate on correct suggestions, and acceptance of wrong ones.

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 5, Options
**Proposed:** Bet on bulk sorting now, with automated suggestions as the next option, gated on results.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Written after reviewing AI suggestions on 26 Oct. Own: the bet, and the point that bulk sorting could raise handler error under pace, which needs to be a health metric. Adopted from AI: the reasoning that bulk sorting changes no decisions and so adds no new automated risk. Reversal condition: if the tail turns out to be information or approval waits, the bet moves to the information flow.

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 6, Spec
**Proposed:** Spec must require a driving-fact reason on every automated pile, a human fallback to reverse or stop payout, and default routing of incomplete or linked claims to a handler.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Rewritten after reviewing AI suggestions on 26 Oct. Own: the reason must cite the facts that drove the decision, not just exist. Adopted from AI: the fallback and default-routing requirements. Still to define: precise meanings of "critical" and "linked".

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 7 and 8, Build and release
**Proposed:** Gates before any claim is paid automatically: shadow period with no money moved, a kill switch with a named owner, and compliance sign-off on reason codes.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Rewritten after reviewing AI suggestions on 26 Oct. Own: the shadow period must cover a month-end pay run. Adopted from AI: the four-week shadow gate, the kill switch and the compliance sign-off. Note: these are gates on the decision to pay automatically, separate from the light build gate for the pull request.
