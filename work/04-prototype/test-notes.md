# Stage 4a test notes

Known limits and decisions, in the order they came up. Read alongside `results.md`.

## The claim set is invented by the AI

The AI wrote the 80 claims, set their correct piles (`labels.csv`) and wrote the rules variant. The handler baseline is simulated.

## Label audit (L1) failed: 50% agreement

On 28 Oct 2026, the human re-labelled 20 claims blind and agreed with the AI labels on 10 (pass ≥ 90%, fail < 80%). K034 was swapped for K058 before the audit, because its label had already been shown.

- 6 claims the human sorted as simple that the AI labelled closer look: duplicates (K001, K054, K059), a paid claim in the last 12 months (K012, K040) and a stale policy check (K016).
- 4 claims the human was stricter on: K019, K024, K070 and K075.

Decision: the human writes a sorting policy (`sorting-policy.csv`), all 80 labels are redone from it, and the human spot-checks them before the test reruns. No labels or results were changed before that.

## Policy start dates are unrealistic (left as is)

The generator gave 67 of the 80 claims the same policy start date, 13 Oct 2023, close to the same day of the year as the claims. This caused at least one misread in the audit: K019 was read as a policy starting the day after the claim. The human chose to leave the data unchanged rather than alter test data after results exist. Any rerun uses the same dates.

## The rules variant shares the sorting policy

The rules were written by the AI alongside its original labels, so they encode much the same judgements that the human's policy later confirmed. The LLM sees only one claim at a time and not the policy. This gives the rules an advantage, which should be weighed when comparing the two. (The rules were not rewritten to the policy; see below.)

## Sorting policy applied (28 Oct 2026)

The human filled in 17 policy rows (`sorting-policy.csv`). All 80 labels were redone from it; 7 changed (K008, K016, K036, K055 to simple under P05; K047, K070, K075 to closer look under P09 and P15). The original AI labels are kept in `labels-v1-ai.csv`. K011 is covered by no row and keeps its simple label.

- **Policy and audit disagree.** Under the human's own policy (P01 duplicates, P02 recent claims), 5 of the human's audit answers would be wrong-simple: K001, K054, K059, K012 and K040. K054 and K059 would pay the same mirror twice. This is Failure 6 (handler over-trust) seen in practice.
- **£1,000 condition in P02 and P03.** No claim in the set has a recent earlier claim under £1,000, so the condition changes no label. A recent claim under £1,000 is a gap in the policy.
- **Spot-check: 10 of 10 after review.** 7 confirmed outright. K054 was marked "no, closer_look", which matches its label. K004 was marked closer look on a sheet that showed only descriptions, not policy dates; with the dates (policy started 8 days before the theft), the human kept suspicious per P11. K052 was marked closer look, then confirmed as simple.
- **The label audit is not re-scored.** It stays recorded as failed at 50% against the AI labels it audited. The new labels are checked by the spot-check, not by a second blind audit, because the policy was written after the human had seen the AI labels.
- **The rules were not updated to the policy.** Changing them after seeing results would be tuning on the test set, so they now miss K075 under P15.

## Grounding check widened before the LLM run (28 Oct 2026)

A one-claim test call showed the LLM citing empty fields as "[] (none)". The grounding check counted that as ungrounded, although it is accurate. Before the full LLM run, the check was changed to accept "[]", "none" or "empty" for a field that is genuinely empty. This changes the measurement, not any variant.

## LLM run and a grounding bug found after it (28 Oct 2026)

The LLM variant (Claude Opus 5.5, medium effort, automatic fallback on) ran once on all 80 claims. No refusals, no fallbacks used, no missing answers. Cost was not measured.

The first scoring reported 88 of 884 cited facts as ungrounded. Part of that was a harness bug: the check compared the AI's text against claim data in which "£" was escaped, so any fact containing "£" failed. Fixing it and rescoring the saved answers (no new API calls) gives 42 of 884. The raw first scoring is kept in `results-llm-run-raw.json`.

The remaining 42 are restatements the substring check can't match, for example "active (checked 2026-10-10)" for the policy status. A sample of 12 read by the AI were all accurate; the other 30 have not been read. The grounding figure is a rough proxy, not a measure of invented facts.

## Stage 4b pilot set-up (28 Oct 2026)

- **Pilot, not the real test.** The human plays the only handler. The real test (5 to 10 handlers with a range of experience, halves swapped between handlers) is described, not run.
- **Claims.** 24 claims from the 37 not yet discussed with the human, in two halves matched on correct pile (5 simple, 6 closer look, 1 suspicious each). The "with suggestion" half includes K035, K065 and K067, which the AI wrongly calls simple, to test over-trust. The halves differ in claim type (3 recent-claim cases with a suggestion, 1 without).
- **The handler isn't fully blind.** The human wrote the sorting policy and has had access to `labels.csv`. The 24 claims weren't discussed, but the human knows how each case type is labelled.
- **Order.** Claims alternate between "with" and "without" in a fixed shuffled order, so tiredness and learning affect both halves alike.
- **AI suggestions re-run with a fuller structure.** The 12 "with" claims were sent to the same model and prompt as in 4a, with extra fields: missing information, investigation needed and next action. All 12 piles matched 4a. Cost about $0.24 (21,497 tokens).
- **Screen fields with no data.** Approval required and linked-claim status aren't in the claim record and are shown as "Not in record". Policy age and days since the last policy check are worked out from the dates and shown alongside them, to avoid the date misread seen in the label audit.
- **Visual style designed by the AI**, per the `SKILL.md` change at the start of 4b. Both conditions use the same layout; only the AI panel differs.
- **A3b limits.** Reclassifications can't be measured in a pilot. Overrides can only happen with a suggestion, so they're reported, not compared. Escalation is counted as "sorted suspicious or escalate ticked".

## Stage 4b pilot result and confounds (28 Oct 2026)

- **Result.** Median time to decide was 61 s with a suggestion and 36 s without, so A3b fails on time. Accuracy was 58% with a suggestion and 83% without. One wrong suggestion was accepted (K035); four correct ones were overridden (K063, K002, K007, K010). Full figures are in `4b-results.md`.
- **Look-alike claims.** The handler suspected duplicates on 7 claims (K002, K007, K010, K026, K037, K042, K069). None is a duplicate in the data. The generator built claims from a few templates, so different claimants have near-identical descriptions (K042 and K032 are word for word the same). Three of the four overrides of correct suggestions cite possible duplicates. Part of the "under-trust" and probably part of the extra time come from the test data, not the suggestion design.
- **Reasons.** The screen made reasons optional without a suggestion and not needed when accepting one. The handler typed reasons on 10 of 12 claims without a suggestion and 6 of 12 with, so reason-typing doesn't explain the slower times.
- **Handler not fully blind, and recording the session.** See the set-up notes above.
