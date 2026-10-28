# Stage 4a results

**Simulation on 80 invented claims. Small sample. Not evidence about real claims.** The AI wrote the claims and the rules variant. The correct piles follow the human's sorting policy (`sorting-policy.csv`), applied to all 80 claims and spot-checked by the human. The handler baseline is invented. See `test-notes.md`.

A3a thresholds (locked at Stage 3): pass if wrong-simple rate ≤ half the handler baseline (3.8%) and zero on linked claims; fail if any wrong-simple on linked claims or a rate above the baseline (7.5%).

| Variant | Accuracy | Wrong-simple | Linked wrong-simple | Over-escalation | Reasons | Ungrounded facts | Median latency | A3a |
|---|---|---|---|---|---|---|---|---|
| handler baseline (simulated) | 85% | 7.5% (6) | 5 of 17 | 7.5% | 0/80 | 0/0 | - | - |
| rules | 89% | 6.2% (5) | 2 of 17 | 5.0% | 80/80 | 0/96 | 0 ms | fail |
| prototype stand-in | 51% | 27.5% (22) | 10 of 17 | 7.5% | 0/80 | 0/0 | 0 ms | fail |
| llm | 69% | 17.5% (14) | 4 of 17 | 6.2% | 80/80 | 42/884 | 6107 ms | fail |

## Label audit (L1), against the original AI labels

Agreement 50%: **fail** (pass ≥ 90%, fail < 80%).

- K001: you simple, AI closer_look
- K012: you simple, AI closer_look
- K016: you simple, AI closer_look
- K019: you closer_look, AI simple
- K024: you closer_look, AI simple
- K040: you simple, AI closer_look
- K054: you simple, AI closer_look
- K059: you simple, AI closer_look
- K070: you suspicious, AI simple
- K075: you closer_look, AI simple

Reason quality is not scored here. It needs the five-point rubric, scored by a human (Failure 3).

