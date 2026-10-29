# Stage 7: build and verify (described, not run)

**AI-drafted** under the process change logged on 29 Oct 2026, for the human to review at the gate. Built from the approved spec (`../06-spec/6-draft.md`) and the Stage 5 decision. Nothing here was built or run. What the squad has already built is not in the brief, so the split below between "built" and "to add" is invented. All durations, targets and retention periods are invented.

Gate weight: light. The gate is the squad's pull request being ready for human review. Merge is the human's decision.

## 1. Implementation

Bulk sorting is assumed to already have a batch view and a "confirm batch" action (invented). The squad adds the spec's controls around it.

| Part | What it does | Spec reference | Owner |
|---|---|---|---|
| Eligibility check | Runs the 8 critical conditions on each claim when a batch is built. Any failure keeps the claim out and records which condition failed. | Section 3, critical | Tech lead and 1 engineer |
| Linked-claim check | Runs rules 1 to 3 against every claim received in the last 90 days, in any pile or status. If the check fails or times out, the claim stays out of the batch. | Section 3, linked | 1 engineer |
| Similar-claims panel | Shows matches under the similar-claim rules next to each claim, as record facts. It doesn't block. | Section 3, similar; 4b requirement 2 | Designer and 1 engineer |
| Batch screen changes | Documents for each claim, the similar-claims panel, pull-out with a required one-line reason, and the batch-level reason shown before confirm. | Stage 5 fixes | Designer and 1 engineer |
| Trace | Writes the batch, claim and human-action records below. | Section 4 | 1 engineer |
| Payment hold and reversal | A hold on a claim or a batch that payment runs respect; a pile change at any time before payment; a recovery case after payment. | Section 5 | Tech lead and 1 engineer |
| Switch-off | A switch for all customers and one per customer, held by the on-call owner. | Rollback below | Tech lead |

**Moves to a later release:** critical item 8 (third party, cash payment, document dates) needs new intake fields, so it's out of this release (the dependency is in spec Section 9). Until it ships, the batch screen tells the handler to check these by eye.

**Open decision for the human:** the controls are added to a build that was due in about six weeks (around 9 Dec 2026). Either the date moves or some controls move later. Of the parts above, only the similar-claims panel tuning could wait without weakening a guardrail; the eligibility check, linked-claim check, trace, hold and switch-off can't.

## 2. Trace format

Every record is written once and never edited; a change writes a new record that points to the old one.

**Batch record:** batch ID, customer, team, handler who confirmed, time built, time confirmed, rule version (eligibility rules, linked rules, similar rules), the batch reason (the eligibility conditions every claim passed), claim IDs in the batch, claim IDs pulled out.

**Claim record (in a batch):** claim ID, batch ID, pile, each check run with its result and the fact values it used (for example "policy status: active, checked 2026-12-10 09:14"), linked-claim check result and the claims searched, similar claims shown, checks not completed.

**Claim record (kept out or pulled out):** claim ID, batch ID, who or what took it out (a named check or the handler), the failed condition or the handler's one-line reason, missing information, next action.

**Human action record (reversal, payment hold, hold lifted, batch pause, switch-off):** action, person, role, time, claim or batch IDs, old and new state, reason, downstream actions triggered.

**Kept:** with the claim, for as long as the customer keeps claim records (each customer's own retention rule), and exportable for a customer or a regulator.

## 3. Rollback path

- **Who:** a named on-call owner each week (for example, the claims product operations lead on call), with the tech lead as backup. Customers can ask for a switch-off for their own organisation through support or their CSM; team leads can pause single batches themselves (spec Section 5).
- **What it does:** bulk sorting stops for all customers or for one. Batches not yet confirmed are dissolved and their claims go back into the normal queue unsorted. Confirmed batches keep their piles. Payment holds are untouched.
- **Review of decisions already made:** the switch-off produces a list of claims sorted in batches over the last 14 days (invented) that haven't been paid, for each customer's team lead to review and hold where needed.
- **Time and test:** target under 5 minutes from decision to bulk sorting stopped (invented). Tested in staging before shadow running starts, with the time measured, and again before each rollout step.

## 4. Verification

| Acceptance criterion (Stage 6) | How it's tested | Evidence in the pull request |
|---|---|---|
| Failure 1: no payment authorised by bulk sorting | Automated test: confirm a batch and check no payment instruction is created | Test output |
| Failure 2: no non-simple claim batched (except critical item 8 kinds) | Run the eligibility and linked checks on the 80 reference claims (invented) | Batch list, showing only K075 as a non-simple claim, with item 8 named |
| Failure 3: every decision has a reason tied to claim fields | Automated test: every batch and claim record has a reason, and every fact value matches the claim | Test output; 10 sample records for compliance |
| Failure 4: linked and duplicate claims caught; failed lookup holds the claim | Seeded tests: K044/K071, K020/K060, N03/N04, the explicit pairs, and a forced lookup failure | Test output |
| Failure 5: missing, stale and invalid inputs kept out | Seeded tests for each of critical conditions 1 to 7, and a forced policy-check failure | Test output |
| Failure 6: 3 of 4 planted claims caught, 10% or fewer simple claims pulled out | Usability test, at least 5 handlers, on the built screen | Results table. Runs on staging; may finish after the pull request opens, but before shadow running |
| Reversal and payment hold | Automated tests: reverse a batched claim; hold a claim 1 minute before a payment run and check it isn't paid | Test output, with timings |
| Batch and claim results reconcile | Automated test: every claim offered to a batch has exactly one outcome record | Test output |
| Switch-off | Staging drill, timed | Drill record with the time |
| 30% time saving | Not testable before release: needs the real baseline and real handlers | Carried to Stage 8 |

## 5. Designer challenge points

- **Can handlers see why a claim is in a batch, and its documents and similar claims, before confirming?** Yes, by design. The test is the usability test in Failure 6. In the bulk pilot, without documents shown, 6 of 9 simple claims were pulled out for "needs photos or estimate".
- **Can they pull out, reverse or hold easily?** Pull-out is one checkbox plus a required reason. Reversal and hold are on the claim page, not only in the batch. Tested by asking handlers in the usability test to reverse one claim and hold one.
- **Further challenge:** a batch of about 15 claims on one screen may be too much to read at pace. The usability test should time handlers per claim and note where they stop reading.

## 6. Engineer challenge points

- **Are the error modes testable?** Yes, each is seeded: a failed or slow linked-claim lookup, a failed policy check, a payment run starting during a hold, and a switch-off with open batches.
- **What does rollback look like in practice?** The switch above, the dissolve-and-requeue of open batches, and the 14-day review list. Drilled in staging and timed.
- **Further challenge:** the linked-claim check searches 90 days of claims for every claim in every batch, which may be slow for large customers (D1-size, about 1,100 handlers). The tech lead should measure lookup time in staging at that volume. A slow lookup must keep the claim out, not let it through.

## 7. Ready for review

- **Ready means:** every automated test in Section 4 passes, the switch-off drill is recorded with its time, 10 sample trace records are attached for compliance, and the usability test is scheduled.
- **Reviewers:** the tech lead and one engineer review the code; the designer reviews the screen; the PM checks the evidence against the Stage 6 criteria. Merge is the human's decision.
- **Open risks carried to Stage 8:** critical item 8 isn't covered; the 30% time saving and Failure 6 are unproven until real handlers use it; the linked-check speed at large-customer volume.
