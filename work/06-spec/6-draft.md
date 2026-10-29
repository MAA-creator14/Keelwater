# Stage 6 draft: spec and acceptance criteria (human draft)

Fill in each section. Short answers are fine. The AI reviews this, then helps tighten the wording and the testable criteria.

Option chosen at Stage 5: **bulk sorting with three fixes** (documents shown for each claim, a similar-claims check, a reason recorded for every batch). The A1 timeline study runs in parallel. AI suggestions stay in discovery. Gate weight: standard.

## Inputs (for reference)

- `../02-failure-map/failure-map.md`: six failure modes, wrong-pay first. Its two open items, "high-risk or ambiguous claims" and "necessary controls or approvals", are now defined in Section 3.
- `requirements-from-4b.md`: a reason on every decision; a similar-claims check.
- `../05-options/decision.md` and `../05-options/assumptions.md`: filter B and the reversal condition.
- Bulk pilot (one person, 13 invented claims): 0 of 4 planted claims spotted, 6 of 9 simple claims pulled out, about 16 s per claim. The two linked claims passed filter B because no related claim was recorded.
- SKILL.md Stage 6 must-haves: the spec is built from the failure map and acceptance criteria, not a feature list; every automated pile carries a reason citing the facts that drove it; a human can reverse a decision or stop a payout at any time; incomplete and linked claims go to a human by default, with "critical" and "linked" defined precisely enough to test; rejected options listed as non-goals.

## 1. Problem and scope

- The problem this release solves, in one or two sentences: Claims handlers need to sort eligible claims efficiently without missing critical documents, relevant linked claims or important risk signals. Bulk sorting should reduce repetitive handling while preserving explainable decisions, human control and safe exception handling.
- Who uses it (handler, team lead, compliance, other): Claims handlers: review batches, investigate exceptions and correct sorting decisions. Team leads: monitor batch progress, handle escalations and stop processing when necessary.
   Compliance or risk reviewers: inspect decision reasons, evidence and audit records.
- In scope: Bulk sorting of eligible claims using the selected sorting rules. Displaying required documents and relevant claim information for each claim. Checking for similar or linked claims before a sorting decision. Recording a reason and supporting facts for every batch decision. Human review, correction, escalation, stopping and audit logging.
- Out of scope for this release: Automatic payment authorisation or payment execution. AI-suggested sorting as a released feature. Automatic resolution of missing information or suspicious claims. Redesigning the entire claims workflow or payment process.

## 2. Failure modes this spec must guard against

For each failure mode that applies to bulk sorting, say what the product does about it. Mark any that don't apply, and why.

| # | Failure | What the product does | Acceptance criterion (testable) |
|---|---|---|---|
| 1 | Wrong payout decision | Separates sorting from payment authorisation. Keeps claims with critical risk signals or unresolved checks out of the eligible batch.| No claim is paid or authorised for payment by the bulk-sorting workflow. All planted critical-risk cases are held for human review.|
| 2 | Wrong pile, no money out | Applies the approved sorting policy consistently and records the assigned pile for each claim.| All defined boundary cases produce the expected pile in automated tests. On the 80 reference claims (invented), the eligibility checks put no non-simple claim into a batch, except kinds listed under critical item 8 (today only K075). In shadow running on real claims, wrong-simple on batched claims is at or below half the handler baseline, and zero on linked claims (the A3a bar).|
| 3 | Missing or incorrect explanation | Records a reason and supporting evidence for every claim-level decision and the batch outcome.| 100% of completed batch decisions have a non-empty reason linked to actual claim fields. Unsupported evidence fails the test.|
| 4 | Missing context (linked, duplicate, earlier claims) |Checks relevant linked claims, duplicate claims and earlier claim history before sorting. |All seeded linked-claim and duplicate scenarios are detected by the test suite. If a required relationship cannot be verified, the claim is held for human review. |
| 5 | Stale or partial inputs | Validates required fields, documents and policy-status freshness before a claim can enter a batch.| All seeded missing, stale and invalid-input cases are excluded from normal batch processing and routed to the defined exception path.|
| 6 | Handler over-trust or error at pace |Makes recommendations and evidence visible, supports corrections, and provides a batch stop control. | Usability test with at least 5 handlers, each sorting a batch of about 15 claims with 4 planted claims the system's checks can't catch (similar-only matches; third-party, cash and document-date cases). Pass: every handler pulls out at least 3 of 4 planted claims, and pulls out 10% or fewer of the simple claims unnecessarily. Handlers can stop a batch. Both thresholds invented; they are kept together because pulling out everything would pass the first alone.|

## 3. Definitions (precise enough to test)

- **Incomplete claim:** a claim missing one or more fields or documents required by the approved sorting policy.
- **Critical** (which missing fields or documents block a claim from a batch): a risk signal or missing requirement that makes automatic inclusion in a normal sorting batch unsafe. Any one of these keeps a claim out of a batch and routes it to a handler (AI-proposed at Stage 6 review; thresholds invented; claims and compliance owners confirm before release):
  1. Policy number missing (P06).
  2. A document the claim type requires is marked missing (P06). A document marked "not required" doesn't block.
  3. Policy status is not "active" at a live check run when the batch is built, or the check fails.
  4. Policy started 60 days or fewer before the incident (P11, P12).
  5. Any claim by the same claimant in the 12 months before this one (P02, P03).
  6. Any match under the linked-claim rules below, or the linked-claim check didn't complete (P08, P09).
  7. Amount £1,000 or more (filter B).
  8. Third party involved, cash payment requested, or a document dated before the incident (P07, P13, P14, P15). These have no structured field today, so until intake captures them, the spec can't test them (dependency, Section 9).
- **Linked claim** (what counts as linked, including links not yet recorded in the system): a claim connected through a verified relationship in Keelwater's data, including links discovered through an approved lookup. A failed lookup is not evidence that no link exists. Two claims are linked if any of these hold (AI-proposed; windows invented):
  1. One lists the other in its related claims, or they share an incident reference.
  2. The same vehicle registration appears in both (in a structured field or the description), with incident dates within 3 days of each other.
  3. The same claimant or the same policy number, with incident dates within 30 days of each other.

  The check searches every claim received in the last 90 days (invented), in any pile and any status, including closed claims. Test cases: the hidden pairs K044/K071 (LK70 YLP, Brook Way) and K020/K060 (HP43 ELB, Chapel Lane), and the bulk-pilot pair N03/N04 (LM19 KTR, Station Street). None of these had a related claim recorded; all are caught by rule 2. Checked on the 80 invented claims: rules 1 to 3 flag exactly the 17 linked claims, and no other claims. A fourth rule (same line, same date, same road) was tried and moved to "similar claim", because on its own it flagged 4 simple claims (K010, K024, K076, K079), partly because the invented claims reuse a small set of roads.
- **Batch eligible** (filter B as is, or changed): a claim that passes the approved completeness, freshness, relationship and risk checks. Eligibility permits sorting only, not payment.
- **Wrong payout:** an incorrect payment outcome or amount. Keep this separate from a wrong sorting pile; one does not automatically prove the other.
- **Similar claim:** a claim that doesn't meet the linked-claim rules but matches on either of these (AI-proposed; windows invented): the same line and the same road or location with incident dates within 7 days; or the same line and an amount within 5%, received within 14 days. Similar claims are shown to the handler as record facts next to the claim; they don't block the batch. The handler decides, and pulling a claim out for a similarity needs a one-line reason. Similarity alone must not be treated as evidence of fraud.
- **High-risk or ambiguous claims:** Claims with critical risk indicators, conflicting or insufficient information, missing or stale evidence, or linked/duplicate claims that could materially change the sorting decision must be excluded from normal bulk sorting and routed to a human for review.
- **Necessary controls or approvals:** Bulk sorting must enforce mandatory document, policy and linked-claim checks, record an evidence-based reason for every decision, and require authorised human review for exceptions, with a human able to stop the batch or reverse a decision; it must never authorise payment.

## 4. Reasons

- What reason a batch decision records, and what makes it one a customer or regulator could follow: batch ID, claim ID, assigned pile, reason, supporting facts, relevant linked claims, checks performed, checks not completed, timestamp and rule/version identifier.
- What a pulled-out claim records: why it was excluded, which check failed, what information is missing and what action the handler needs to take.
- Who signs off the reason format, and when: the claims/risk owner approves the reason format and compliance requirements before release.

## 5. Human control

- How a handler or team lead reverses a sorting decision, and within what time: an authorised handler can change a claim's pile, record a reason and preserve the original decision and evidence. Any handler or team lead can do this on any claim at any time before payment, with no time limit, including claims in batches already confirmed. The new pile reaches downstream systems within 1 minute (invented target). After payment, a reversal opens a recovery case instead (out of scope for this release).
- How someone stops a payout on a claim sorted in a batch, and who can: the handler or team lead can pause processing immediately. Separately, any handler, team lead or compliance reviewer can put a **payment hold** on a single claim, or on every claim in a batch, at any time until the payment is made, including batches confirmed earlier. A held claim is left out of every payment run until the hold is lifted, and lifting a hold needs a team lead and a one-line reason. Test: a hold placed 1 minute (invented) before a payment run keeps the claim out of that run. When a batch is paused, claims not yet sorted stay unsorted in the queue; claims already sorted in that batch keep their pile, are not held automatically, and are listed for the team lead to review and hold where needed.
- What gets logged when either happens: log both events, record the person, timestamp, original and new status, reason, batch ID and any downstream actions required.

## 6. Acceptance criteria for the release

The criteria the squad's build must meet before Stage 7 closes. Include thresholds and say which are invented.

All six failure-mode test groups pass, including the seeded linked-claim, duplicate, missing-data and stale-data cases.
- Every automated sorting decision has a reason and traceable supporting evidence.
- No payment is authorised or executed by the bulk-sorting workflow.
- Ineligible claims are excluded and routed to the defined human-review process.
- Handlers can override decisions and stop a batch, with all changes recorded.
- Batch-level and claim-level results reconcile: every input claim has a traceable outcome, including exceptions.
- Handler time per batched claim is at least 30% lower than the real baseline measured before release (the A3b bar; invented), with the Failure 2 and Failure 6 guardrails no worse.

## 7. Measures after release

- Primary measure: Median handler time to complete correct sorting, compared with the measured baseline.
- Secondary measures, tracked with no target until A1 reports: share of claims taking more than four hours to sort (15% in the brief), and median and 90th-percentile time to correct payment. If A1 shows the queue is 15% or less of that time, bulk sorting isn't expected to move the tail.
- Guardrails (with thresholds): Wrong-pile rate, per-pile confusion matrix and dangerous misclassifications; wrong-simple on batched claims at or below half the handler baseline and zero on linked claims; simple claims pulled out unnecessarily 10% or less (invented).
- What would make you pull or pause bulk sorting:
  - **Immediate pause:** any wrong payout traced to a batched claim, or any linked claim found in a confirmed batch.
  - **Review and pause:** the number of incorrect decisions, payment errors, reversals, reclassifications and incidents on batched claims rises by 10% or more against the pre-release baseline, over a rolling 2-week window with at least 500 batched claims (window and volume invented). Reclassifications take up to 30 days to show, so payment holds and handler reversals act as the early signal.

## 8. Non-goals (rejected options, one line each)

- Auto-clear of simple claims: explicitly excluded; all three variants (rules, prototype stand-in, LLM) failed A3a at Stage 4a, and this release does not authorise payment.
- AI-suggested sorting in this release: remains in discovery because the Stage 4b pilot showed potential over-reliance and slower decisions.
- Automatic investigation of fraud decisions: the system routes claims for review; it does not make unsupported fraud determinations.

## 9. Open questions and dependencies

- A1 timeline study (what changes in this spec if the queue is 15% or less): If the timeline study shows queueing accounts for 15% or less of total elapsed sorting time, do not assume queue management is the main opportunity. Reassess the specification against the measured causes of delay, including active handling, information waits and approval waits. Revise the scope if bulk sorting does not address the dominant cause.
- Other: 
- Claims and compliance owners must define critical signals and required approvals.
- Intake needs structured fields for third party involved, payment method requested and document dates, so critical item 8 can be tested. Until then, claims of these kinds can still reach a batch (the bulk pilot's wall-damage claim did).
- The linked-claim data source must reliably identify relevant relationships.
- The bulk-sorting implementation must support per-claim traceability and batch stopping.
- The linked-claim matching rules (Section 3) must catch hidden pairs such as K044/K071, K020/K060 and the bulk-pilot pair N03/N04, none of which had a related claim recorded.
- A real baseline for handler time and guardrails must be measured on real claims before release. The 36 s figure is one person on a mock screen with invented claims.
