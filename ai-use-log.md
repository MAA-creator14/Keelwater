# AI use log: keelwater-sorting

Append-only. One entry per AI session that affects the Keelwater work. Keep the "kept / changed / rejected" lines in your own words. Fill in every bracketed line before the panel pack goes out, and set each timestamp to the real time you logged it.

## 2026-10-25T19:45:00Z - Item: keelwater-sorting - Stage 0: AI use
**Asked:** Summarise the Keelwater task and say what it is testing.
**Got:** A reading of the brief: the panel judges how I got there, not the output; three things to test (question the request, use the data, sequence under pressure).
**Kept / changed / rejected:**
- Kept: the framing that the panel judges process over output.
- Rejected: left out Xelix specific points from interview on 21 October.
**Evidence:** Chat, 25 Oct, first turn.

## 2026-10-25T19:55:00Z - Item: keelwater-sorting - Stage 0: AI use
**Asked:** Critique my AIPDLC skill as a process for this task.
**Got:** Seven criticisms, including no assumptions register, no sequencing or stop decisions, and gates too literal for "proportionate" discovery. Revised eight-stage shape proposed.
**Kept / changed / rejected:**
- Kept: the assumptions register, and the stop and sequencing stage.
- Changed: moved the failure map ahead of evidence and assumptions, because what can go wrong should shape what we test.
- Rejected: that the gates were too literal. I kept a gate at every stage and added light, standard and formal weights instead.
**Evidence:** Chat, 25 Oct, revised stage order.

## 2026-10-26T06:15:00Z - Item: keelwater-sorting - Stage 0: AI use
**Asked:** Explain instinct notes, give failure-mode examples, critique my Stage 3 assumption and thresholds.
**Got:** Seven failure modes with step and check; two alternative riskiest assumptions (handler trust, explainability) and placeholder thresholds.
**Kept / changed / rejected:**
- Kept: queue-versus-waiting as the riskiest assumption, with a four-way time split.
- Changed: kept the 60-claim sample and the 30% and 15% thresholds, but sample from the last 12 months only if the data is clean enough to classify time spent.
- Rejected: handler trust and explainability as the riskiest assumption, because if the tail is information or approval waits rather than queue time, sorting doesn't help and neither of them matters.
**Evidence:** Chat, 26 Oct; aipdlc-log.md, Stage 3 entry.

## 2026-10-26T19:12:00Z - Item: keelwater-sorting - Stage 0: AI use
**Asked:** Check whether the rewritten Stage 4a to 8 notes were recorded before AI output.
**Got:** Flagged that the rewritten notes mirror the examples given, so they can't be logged as clean pre-AI instinct. Proposed a post-exposure label and a fix list.
**Kept / changed / rejected:**
- Kept: post-exposure labelling, and doing each stage's own work myself before asking the AI to review it.
- Kept for stages 7 and 8: the shadow-period gate, the kill switch and the compliance sign-off on reason codes.
- Rejected: the other suggestions for stages 7 and 8, as I preferred my own thinking and writeup.
**Evidence:** Chat, 26 Oct; aipdlc-log.md, Stage 4a to 8 entries marked post-exposure.

## 2026-10-27T08:15:00Z - Item: keelwater-sorting - Stage 1: AI use
**Asked:** Use synthetic data to invent support, sales and CS tickets.
**Got:** Data for 40 support tickets, 6 sales deals and 3 CS tickets as well as a coding sheet. 
**Kept / changed / rejected:**
- Kept: Kept the ticket and role data as generated.
- Changed: Open coded the tickets myself.
- Rejected: Confidence level per ticket. Having reviewed the tickets, I felt that adding confidence levels would not add much weight in this instance.
**Evidence:** Chat, 27 Oct; aipdlc-log.md, Stage 1 entry.

## 2026-10-27T12:01:01Z - Item: keelwater-sorting - Stage 2: AI use
**Asked:** Critically review three proposed failure modes.
**Got:** A review of my 3 proposed failure modes, plus 4 missing modes suggested by the AI.
**Kept / changed / rejected:**
- Kept: missing context, stale or partial inputs and handler over-trust failure modes.
- Changed: narrowed Failure 2 to errors with no money moved.
- Rejected: drift failure mode because I don't believe the claim mix to be a real factor.
**Evidence:** Chat, 27 Oct; aipdlc-log.md, Stage 2 entry.

## 2026-10-28T07:03:01Z - Item: keelwater-sorting - Stage 3: AI use
**Asked:** Review 3 riskiest assumptions in Assumptions Register.
**Got:** A critical review of my assumptions, tresholds, pass and fail outcomes.
**Kept / changed / rejected:**
- Kept A1 assumption.
- Changed: treshold conditons for A1 and A3
**Evidence:** Chat, 28 Oct; aipdlc-log.md, Stage 3 entry.

## 2026-10-28T18:42:01Z - Item: keelwater-sorting - Stage 4a: AI use
**Asked:** Review my draft system test and proposed planted faults
**Got:** Invented a handler baseline and invented 80 claims
**Kept / changed / rejected:**
- Kept invented claims
- Changed the sorting policy
- Rejected the reason quality rubric suggestion, logged as not done to focus on sorting accuracy instead
**Evidence:** Chat, 28 Oct; aipdlc-log.md, Stage 4a entry.

## 2026-10-28T18:42:01Z - Item: keelwater-sorting - Stage 4b: AI use
**Asked:** Review my draft for a UI for handlers to review AI generated suggestions
**Got:** A simple handler UI for coding a mix of claims
**Kept / changed / rejected:**
- Kept the suggestion to test as a single handler (instead of 5-10)
**Evidence:** Chat, 28 Oct; aipdlc-log.md, Stage 4b entry.

## 2026-10-28T20:11:01Z - Item: keelwater-sorting - Stage 5: AI use
**Asked:** Review my proposed approach to testing bulk sorting
**Got:** Suggestions on how to sharpen the test
**Kept / changed / rejected:**
- Kept: proposed assumptions with ranges labelled invented assumptions (time per batch, error rate under pace, etc.)
- Changed the filter (any type under £1,000)
- Rejected recommended suggestion to finish building bulk sorting and running A1 study, opting for an approach that enables me to do further discover and codesign AI suggestions iterations
**Evidence:** Chat, 28 Oct; aipdlc-log.md, Stage 5 entry.
