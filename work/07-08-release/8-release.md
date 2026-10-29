# Stage 8: release and measure (described, not run)

**AI-drafted** under the process change logged on 29 Oct 2026, built on the human's calls: a named on-call owner holds the switch-off; 2 weeks of shadow running, then one team, then everyone; go/no-go by the PM with the claims owner; Sales and CS told now, with limits; C-008's team goes first after shadow. All dates, durations and volumes are invented. Customer details come from the invented signals in `../01-signals/`.

Gate weight: formal.

## Why SKILL.md's three formal gates don't apply as written

SKILL.md sets three gates "before any claim is paid automatically": a shadow period covering a month-end pay run, a tested kill switch, and compliance sign-off on auto-cleared claims. In this release no claim is paid automatically (auto-clear was ruled out at Stage 4a). So the release plan below keeps what still applies: shadow running before handlers rely on it, a tested switch-off with a named owner, and compliance sign-off on the reason format. It drops the month-end requirement, which is about money moving automatically.

## 1. Baselines

Measured on real claims before shadow running starts, for each customer in the rollout:

- Handler time per claim on the real screen (replaces the 36 s from one person on a mock).
- Wrong-simple rate and per-pile confusion matrix, from a senior-handler review of a sample (sample size set with the claims owner).
- Reversals, reclassifications within 30 days, and payment holds.
- Share of claims taking more than four hours to sort (15% in the brief), and median and 90th-percentile time to correct payment.

## 2. Rollout

| Step | What happens | Length | Go/no-go before it |
|---|---|---|---|
| 0. Drill | Switch-off drilled in staging and timed; trace records reviewed by compliance | Before shadow | Switch-off under 5 minutes; compliance signs off the reason format (spec Section 4) |
| 1. Shadow | Batches are proposed but not used: handlers sort as usual. Each proposed batch is compared with what handlers did, and a senior handler reviews a sample | 2 weeks | Step 0 passed |
| 2. One team | One C-008 team uses bulk sorting, with feedback sessions run by the PM and designer | 2 weeks | Shadow: no non-simple claim in a proposed batch other than critical item 8 kinds; no linked claim batched |
| 3. Everyone | All customers, in waves of about a fifth of customers a week | About 5 weeks | Step 2 meets the Stage 6 criteria, including the 30% time saving and Failure 6 |

The PM and the claims owner both sign each go/no-go; either can say no. Each decision is logged in `aipdlc-log.md`.

**Limits of a 2-week shadow:** reclassifications take up to 30 days to show, so shadow running checks eligibility, not later corrections; the senior-handler sample fills the gap. It also may not include a storm surge, which is when C-008 needs it most (T03, T16). If the build ships around 9 Dec 2026, shadow running falls over Christmas, when volumes and staffing are unusual. Starting shadow on 4 Jan 2027 avoids that (an open decision for the human).

## 3. Guardrails and kill criteria

From the spec (Sections 6 and 7):

- **Immediate pause:** any wrong payout traced to a batched claim, or any linked claim found in a confirmed batch. The on-call owner switches off for that customer, or all customers if the cause isn't customer-specific.
- **Review and pause:** a rise of 10% or more in incorrect decisions, payment errors, reversals, reclassifications or incidents on batched claims, against the pre-release baseline, over a rolling 2 weeks with at least 500 batched claims.
- **Early signals:** payment holds and handler reversals on batched claims, reviewed weekly.
- **Remediation is never automatic.** A switch-off stops bulk sorting; what to do about claims already sorted is decided by people, using the 14-day review list.

## 4. Measurement plan

- **Weekly during rollout:** guardrails, holds and reversals by customer; handler time per batched claim against the baseline; share of claims pulled out, and why.
- **At 30 days after general release:** reclassifications of batched claims against the baseline; share of claims over four hours; time to correct payment.
- **When A1 reports:** if the queue is 15% or less of four-hour time, record that bulk sorting isn't expected to move the tail, and move the main effort to the information and approval flow (the Stage 5 reversal condition).

## 5. Sales and Customer Success schedule

**What they must not promise:** automatic sorting, or faster payment (including any 24-hour payment target). Bulk sorting is handlers sorting many simple claims at once, with a reason recorded for every decision.

| When | Who | What |
|---|---|---|
| Now (week of 2 Nov 2026) | Sales and CS leads | What's coming and roughly when; the two things not to promise; that AI-assisted sorting is in discovery with no date. A one-page brief and a short Q&A with the PM |
| Now | C-008's CSM | C-008's team goes first after shadow running, well before the March 2027 renewal. Frame it around their volume spikes and Monday backlogs (T03, T16, T26), not automation |
| Now | D1's rep | D1's RFP asks for "AI-assisted triage, with an explainable reason recorded for every decision" (requirement 14). Bulk sorting meets the second half, not the first. The rep answers honestly: the reason records are coming; AI-assisted triage is in discovery. Offer a demo of the reason records |
| Now | C-012's CSM | Their auditor found sorting decisions have no recorded reason. Offer their compliance officer an early look at the reason format |
| After shadow (mid-Jan 2027) | Sales and CS | Shadow results in plain terms; D1 demo of reason records, ahead of their January decision |
| At one-team step | CS | C-008 feedback; dates for the waves |
| At general release | Sales, CS, Support | Release notes; what handlers will see; how to ask for a switch-off |
| When A1 reports | Sales and CS | What it means for the roadmap, including AI suggestions |

## 6. Open decisions (as decided at the Stage 7 and 8 gates, 29 Oct 2026)

- Build date versus scope: decided by the human after the tech lead's estimate.
- Shadow start date: set after that estimate. The Christmas period is a known risk.
- Senior-handler review sample size: agreed with the claims owner before shadow running starts.
