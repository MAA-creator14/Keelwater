# AIPDLC log: keelwater-sorting

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 1, Frame the signal
**Proposed:** Problem framing: the slow tail, not the average, is the problem to solve.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Written after reviewing AI suggestions on 26 Oct. Own view: the median of 11 minutes is already fast, so the problem is the long tail (15% over four hours). Confidence in the 15% figure is high because it is in the brief; confidence in its cause is low. Adopted from AI: none. Not yet tested: whether the tail is a sorting problem.
**Confidence level:** low, in the cause of the tail (high in the 15% figure itself)
**What would surprise me:** If the tail was a sorting problem, handlers not knowing what to do with the relevant claims. 

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 2, Failure map
**Proposed:** Two expected failure families: wrong pile on claims that look simple, and right pile with the wrong reason.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Written after reviewing AI suggestions on 26 Oct. Own: the "claimant has had an accident before" case, a concrete example of the first family. Adopted from AI: the two-family structure and the wrong-reason example. Still to add: which of these handlers would recognise first.
**Confidence:** medium
**What would surprise me:** If a large number of failures were due to handlers not following internal policies and approval processes.

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 3, Evidence and assumptions
**Proposed:** Riskiest assumption: the four-hour wait is caused by information or approval waits, not by the queue.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Written after reviewing AI suggestions on 26 Oct. Own: the assumption itself and why it is the riskiest, because if it is true, sorting automation does not help the tail. Adopted from AI: the 60-claim sample, the four time categories, and the 30% and 15% thresholds. Own change to make before the test: sample from the last 12 months only if the data is clean enough to classify time spent. The threshold percentages are invented, used to measure the queue time: if the queue or unworked time accounts for more than 30% of 4 hour claims, then automated sorting will have the desired impact on resolution speed. If it is 15% or less we can conclude that sorting is not the right problem to solve.
**What would surprise me:** If the 15% of four-hour wait instances were solely the result of internal inefficiencies (e.g. resource capacity planning or constraints). 

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 4a, System test
**Proposed:** Rules-based variant expected to have the lowest wrong-pay rate; LLM classifier expected to miss linked-claim context.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Rewritten after reviewing AI suggestions on 26 Oct. Own: the rules variant will be more cautious and raise more false positives for handlers. Adopted from AI: the expectation that the LLM misses linked claims, and the linked-claim subset as the test. Check that would prove this wrong: wrong-pay on the linked-claim subset, reported separately from the overall rate.
**Confidence:** medium 
**What would surprise me:** If there is no significant impact on sorting time median when applying LLM classifier.

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 4b, UI mock
**Proposed:** Handlers will not immediately trust automated suggestions; the UI needs to make override easy.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Rewritten after reviewing AI suggestions on 26 Oct. Own assumption: handlers will not trust suggestions by default. Adopted from AI: the override-as-trust-mechanism idea. To test: override rate on correct suggestions, and acceptance of wrong ones.
**Confidence:** high
**What would surprise me:** If the number of overrides doesn't go down over time, assuming that the interface and context provided to the handler will instill confidence.

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 5, Options
**Proposed:** Bet on bulk sorting now, with automated suggestions as the next option, gated on results.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Written after reviewing AI suggestions on 26 Oct. Own: the bet, and the point that bulk sorting could raise handler error under pace, which needs to be a health metric. Adopted from AI: the reasoning that bulk sorting changes no decisions and so adds no new automated risk. Reversal condition: if the tail turns out to be information or approval waits, the bet moves to the information flow.
**Confidence:** low
**What would surprise me:** If the bulk sorting does not bring down the median throughput time by at least a few minutes.

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 6, Spec
**Proposed:** Spec must require a driving-fact reason on every automated pile, a human fallback to reverse or stop payout, and default routing of incomplete or linked claims to a handler.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Rewritten after reviewing AI suggestions on 26 Oct. Own: the reason must cite the facts that drove the decision, not just exist. Adopted from AI: the fallback and default-routing requirements. Still to define: precise meanings of "critical" and "linked".
**Confidence:** high 
**What would surprise me:** If no errors are identified in reasons provided, e.g. policy typos or applying incorrect reasons.

## 2026-10-26T19:17:00Z - Item: keelwater-sorting - Stage: Stage 7 and 8, Build and release
**Proposed:** Gates before any claim is paid automatically: shadow period with no money moved, a kill switch with a named owner, and compliance sign-off on reason codes.
**Decision:** Instinct recorded (post-exposure)
**Notes:** Rewritten after reviewing AI suggestions on 26 Oct. Own: the shadow period must cover a month-end pay run. Adopted from AI: the four-week shadow gate, the kill switch and the compliance sign-off. Note: these are gates on the decision to pay automatically, separate from the light build gate for the pull request.
**Confidence:** medium
**What would surprise me:** If no compliance issues are detected post-release, use guardrails and traces to identify and correct.

## 2026-10-27T08:09:00Z - Item: keelwater-sorting - Stage: Stage 1, Frame the signal
**Proposed:** Problem statement: 15% of claims take 4+ hours to sort, appearing mostly due to waits for missing information or approval, affecting 315,000 claims a year.
**Decision:** Edited
**Notes:** Added missing word "be". Approved despite gaps: no cost or who-bears-it in the statement, and no confidence levels in the coding. Source material invented by AI; coding by human.

## 2026-10-27T11:55:00Z - Item: keelwater-sorting - Stage: Stage 2, Failure map
**Proposed:** Six failure modes, wrong-pay first: 3 human-drafted, plus missing context, stale or partial inputs and handler over-trust added at AI review.
**Decision:** Approved
**Notes:** Failure 2 narrowed to errors with no money out. Drift offered and not kept. Failure 1 terms and the noisy handler labels carried to Stage 3.


## 2026-10-28T06:59:00Z - Item: keelwater-sorting - Stage: Stage 3, Evidence and assumptions
**Proposed:** Register of 5 rows (A1 waits not queue, A2 overlooked information, A3a AI accuracy, A3b AI value, L1 label audit), ranked, with thresholds set before any test.
**Decision:** Approved
**Notes:** Thresholds locked. A1 keeps the Stage 0 queue-time 30%/15%, reversed so queue ≤15% passes. A3 split by AI; A2 and A3 redrafted by AI and edited by human. Label audit (L1) runs before A3a.

## 2026-10-28T16:32:00Z - Item: keelwater-sorting - Stage: Stage 4a, System test
**Proposed:** Three variants on 80 invented claims (simulation): rules 6.2% wrong-simple, 2 linked; prototype stand-in 27.5%, 10 linked; LLM 17.5%, 4 linked. Handler baseline 7.5% (simulated). All fail A3a.
**Decision:** Approved
**Notes:** Outcome: revise. AI may only route claims toward a human; auto-clear dropped. Planted faults: both found. L1 failed (50%); labels rebuilt from human sorting policy and spot-checked. Reason rubric not done. Limits in work/04-prototype/test-notes.md.

## 2026-10-28T18:21:00Z - Item: keelwater-sorting - Stage: Stage 4b, UI mock
**Proposed:** One-person pilot, 24 invented claims: 61 s with suggestion vs 36 s without; accuracy 58% vs 83%; 1 of 3 wrong suggestions accepted, 4 of 9 correct ones overridden. A3b fails on time.
**Decision:** Approved
**Notes:** Fail carried to Stage 5; suggested sorting stays in the comparison. Templated look-alike claims confound overrides and time. Visual design (AI-designed; SKILL.md changed to help communication with customers, Sales and CS) approved with changes: required reasons and a similar-claims check, carried to Stage 6.

## 2026-10-28T20:08:00Z - Item: keelwater-sorting - Stage: Stage 5, Options
**Proposed:** Four options on 80 invented claims: status quo 6 wrong-simple, 36 s; bulk 5.2–6.0, 26–37 s (pilot: 0 of 4 planted claims spotted, 6 of 9 simple pulled out); suggested 61 s, 1 of 12 (pilot); auto-clear 5–14, ruled out.
**Decision:** Approved
**Notes:** Bulk ships with fixes; A1 timeline study in parallel; suggestion discovery with Sales and design partners, no engineering time. Weights: 6 standard, 7 light, 8 formal. Reverse if A1 queue ≤15%: effort moves to information and approval flow.

## 2026-10-29T18:36:00Z - Item: keelwater-sorting - Stage: Stage 6, Spec
**Proposed:** Spec for bulk sorting with three fixes: critical list (8 conditions), linked rules 1–3 (flag exactly the 17 linked of 80 invented claims), per-claim payment hold and reversal any time before payment; invented thresholds (3 of 4 planted spotted, ≤10% simple over-pulled, ≥30% time saved, two-level pause); non-goals auto-clear, AI suggestions, automatic fraud decisions.
**Decision:** Approved
**Notes:** Human drafted; definitions, human-control items and thresholds AI-proposed at review and accepted. Critical item 8 untestable until intake captures third party, payment method and document dates. Time to payment tracked with no target until A1 reports.

## 2026-10-29T18:49:00Z - Item: keelwater-sorting - Stage: Process change
**Proposed:** From Stage 7, AI drafts first because of time; the human makes the named judgment calls (rollback owner, rollout and shadow period, go/no-go owner, Sales and CS timing and limits, design-partner access) and decides each gate.
**Decision:** Approved
**Notes:** Departs from the 26 Oct commitment to draft each stage before AI review. Stages 1 to 6 were human-drafted.

## 2026-10-29T19:53:00Z - Item: keelwater-sorting - Stage: Stage 7, Build and verify (described)
**Proposed:** AI-drafted build description: seven controls with owners, append-only trace format, switch-off by a named on-call owner (under 5 minutes, invented, drilled in staging), verification table mapped to the Stage 6 criteria, designer and engineer challenge points.
**Decision:** Approved
**Notes:** Date versus scope left open: the human decides after the tech lead's estimate. Carried to Stage 8: critical item 8 not covered, 30% time saving and Failure 6 unproven, linked-check speed at large-customer volume.

## 2026-10-29T20:00:00Z - Item: keelwater-sorting - Stage: Stage 8, Release and measure (described)
**Proposed:** AI-drafted release plan on the human's calls: real baselines; drill, 2-week shadow, one C-008 team for 2 weeks, then waves; PM and claims owner sign each go/no-go; two-level kill criteria; Sales and CS told now, no promise of automatic sorting or faster payment. SKILL.md auto-payment gates recorded as not applying.
**Decision:** Approved
**Notes:** Shadow start set after the tech lead's estimate (Christmas a known risk). Review sample size agreed with the claims owner before shadow. D1's RFP asks for AI-assisted triage; bulk sorting meets only the reason-record half.
