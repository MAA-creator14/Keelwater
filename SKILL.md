---
name: keelwater-sorting-aipdlc
description: Run the Keelwater claims-sorting product lifecycle as a human-gated, evidence-led process. Use when the user says "run the keelwater lifecycle", "next stage", "what stage are we on", "log this decision", "log the AI use", or asks to test, compare or decide on automated or bulk claim sorting. Governs the item keelwater-sorting from signal to measurement, with a gate and an audit entry at every stage.
---

# Keelwater Sorting: AI-Driven Product Lifecycle with Human Gates

A governance skill. Claude does the drafting, analysis, coding and checking. The human owns every gate decision, every threshold and every commitment to a customer or to the squad. Claude never advances past a gate on silence, on a vague "continue", or on its own view that the work looks good.

## Item and context

- Item slug: `keelwater-sorting`. Use it in every log heading.
- Log file: `aipdlc-log.md`. Append only. Never rewrite past entries.
- Context file: `context/keelwater.md`. Holds the brief facts (pile definitions, 2.1M claims a year, 11-minute median, 15% over four hours, 3.4% reclassified within 30 days, the explainability requirement) and the metrics: time to correct payment, handler minutes, wrong-pay rate, reversal rate, override rate, and compliance acceptance of reason codes.
- Every number that is not in the brief is invented, and must be labelled "invented" wherever it appears.

## Startup

1. Read the last approved entry for `keelwater-sorting`. Resume at the next stage.
2. If the last entry was rejected or edited with rework, stay on that stage and redo it.
3. If the user names a stage, jump there and log the jump, with the reason.
4. Tell the user which stage you are starting and why before doing any work.

## Stage 0: Instinct (human only)

Before any AI output for a stage, the human writes down: what they think the stage should conclude, how confident they are, and what would surprise them. Claude asks for this and does not draft it. Logged as `Decision: Instinct recorded`. Claude does not proceed to Stage 1 without it.

## Stage 1: Frame the signal

- Do: Code the 40 tickets, sales notes and CS notes by underlying need, not by the word "sorting". Separate the request (automatic sorting) from the problem beneath it. Give a confidence level for each reading, using the Confidence Meter scale: opinion and trend near zero, anecdote low, quantified behaviour higher.
- Gate, standard weight: the human confirms the problem statement in one sentence, naming who has it and what it costs. If the statement is a feature, the stage fails.

## Stage 2: Failure map

- Do: List where the output can be wrong, by step: wrong pile with confidence, right pile with a wrong or missing reason, missing context, stale or partial inputs, drift. For each mode, name the step where it occurs and the test that would catch it.
- Gate, standard weight: the human keeps the failure modes handlers would recognise and adds any Claude missed. Wrong-pay is always ranked first.

## Stage 3: Evidence and assumptions

- Do: Build the assumptions register: assumption, type (problem, trust, explainability, accuracy, value, feasibility), risk if wrong, cheapest test, pass/fail threshold, and what would change the plan. Check the label quality of the reclassification measure by auditing a sample with a senior handler.
- Gate, standard weight: the human ranks the assumptions and sets thresholds. Thresholds must be logged before the test runs. A threshold set after seeing results is rejected and the stage is redone.

## Stage 4: Prototype and test

Two sub-tests, each with its own gate.

- 4a. System test: three quick variants on the same synthetic claim set (about 80 claims, stratified, with hard cases over-sampled; all invented): rules baseline, the old predictive prototype, and an LLM classifier that returns a pile and a reason. Measure pile accuracy, wrong-pay rate (overall and on the linked-claim subset, reported separately), reason quality on a five-point rubric, and latency. Also test data completeness, staleness and duplicates. Claude may build the harness and the first agent, then runs a review pass on its own code. The review is only credible if a planted fault is caught, so Claude plants one and reports whether it was found.
- 4b. UI mock: a simple suggestion screen showing pile, plain-English reason, accept and override controls, with a required one-line reason on override. Record accept, override and time to decision, with and without the suggestion. Claude may design the mock's visual style; the human approves it at the 4b gate. (Changed on 28 Oct 2026 at the start of Stage 4b, because a more visually appealing design helps when communicating with customers, Sales and Customer Success. Until then, Claude did not design the visual style.)
- Gate, formal weight for 4a, standard for 4b: the human checks the review, checks the results against the pre-set thresholds, and decides whether the result is a pass, a revise, or a stop. A result is labelled as a simulation with a small sample wherever it is shown.

## Stage 5: Options and decision

- Do: Compare options on one shared test set and one set of measures: status quo, bulk sorting, suggested sorting with human decision, and auto-clear of simple claims. Report efficiency, data output, speed to payment (median and 90th percentile), and guardrails (override rate, escalations, reversals, handler error under pace). Name the trade-off for each option in one sentence. Do not rank a winner: state what the evidence supports.
- Gate, formal weight: the human chooses which option to take forward, names the gate weight for each subsequent stage, and writes what would make them reverse the decision.

## Stage 6: Spec and acceptance criteria

- Do: Write a short spec for the option chosen. It is built from the failure map and the acceptance criteria, not from a feature list. Every automated pile carries a reason that cites the facts that drove it. A human can reverse a decision or stop a payout at any time. Incomplete or linked claims route to a human by default, with "critical" and "linked" defined precisely enough to test. Carry rejected options forward as one line each under non-goals.
- Gate, standard weight: the human approves, edits or rejects. Partial edits are re-confirmed.

## Stage 7: Build and verify (described, not run in this task)

- Do: Describe the implementation for the chosen option, including the trace format, the rollback path and the designer and engineer challenge points: can handlers see and override a suggestion (designer), are error modes testable and what does rollback look like (engineer).
- Gate, light weight: the squad's pull request is ready for human review. Merge is the human's decision. Claude never offers to merge.

## Stage 8: Release and measure (described, not run)

- Do: Define baselines, guardrails, kill criteria and the measurement plan. Draft the Sales and CS communication schedule.
- Gates before any claim is paid automatically, all formal weight:
  1. Shadow period with no money moved, long enough to cover at least one month-end pay run (for example, four weeks), with agreement against handler decisions above a threshold set in advance and no wrong-pay in the high-cost subset.
  2. A named owner holds a kill switch that stops payments and routes claims back to handlers, tested in staging, with the halt time measured.
  3. Compliance has signed off the reason codes on a sample of auto-cleared claims.
- Remediation after a production problem is never automatic. Claude always asks first.

## Audit log format

Append after every gate, after the human responds. Keep it terse.

    ## [ISO 8601 timestamp] - Item: keelwater-sorting - Stage: [stage name]
    **Proposed:** [one line: what Claude put in front of the human]
    **Decision:** Approved | Edited | Rejected | Instinct recorded | Jump
    **Notes:** [a phrase, not a paragraph]

AI-use entries use the same heading with Stage: AI use, and four fields:

- **Asked:** what the human asked the AI to do
- **Got:** what it produced
- **Kept / changed / rejected:** in the human's words, with the reason for any rejection
- **Evidence:** the file or output affected

## Ground rules

- Keelwater only. Do not import material from any other company or case into any output.
- Flag every invented figure, quote and dataset.
- Logs are written when the gate closes, not batched.
- Every loop back to an earlier stage is logged as a jump, with the trigger.
- The human decides. Claude presents evidence, options and risk, and never frames a recommendation as settled.
