# Stage 5 comparison of options

**Simulation on 80 invented claims. Correct piles follow the human's sorting policy. Status quo
handler piles are invented. Bulk-sorting figures are modelled from invented assumptions (low,
middle, high risk), not observed. Pilot timings come from one person.** See
`../04-prototype/test-notes.md` and `assumptions.md`.

Filter B batches 27 of the 80 claims; 1 of
those need a closer look (K075). Claims outside
the batch are sorted as in the status quo. Inside the batch, simple claims are sorted simple unless
pulled out, so the simulated handler's errors on those claims don't carry over.

| Option | Handler time per claim | Accuracy | Wrong-simple | Linked wrong-simple | Over-escalation (simple claims sent for checking) | Data output |
|---|---|---|---|---|---|---|
| Status quo | 36 s (n=12, one person) | 85% | 6 of 80 | 5 of 17 | 6 | Pile and who sorted it; no reason recorded |
| Bulk sorting, filter B (low risk) | 26 s (modelled) | 92% | 5.2 of 80 | 5.0 of 17 | 1.1 | One batch decision; the filter criteria serve as the reason |
| Bulk sorting, filter B (middle risk) | 29 s (modelled) | 92% | 5.5 of 80 | 5.0 of 17 | 1.3 | One batch decision; the filter criteria serve as the reason |
| Bulk sorting, filter B (high risk) | 33 s (modelled) | 91% | 5.8 of 80 | 5.0 of 17 | 1.5 | One batch decision; the filter criteria serve as the reason |
| Bulk sorting, filter B (pilot-observed) | 37 s (modelled) | 87% | 6.0 of 80 | 5.0 of 17 | 4.3 | One batch decision; the filter criteria serve as the reason |
| Suggested sorting, human decides | 61 s (n=12, one person) | 58% (n=12) | 1 of 12 | not tested in pilot | see 4b | Pile, structured AI reason, facts, missing information, override reason |
| Auto-clear (ruled out at 4a) | 6 s machine (LLM) | LLM 69%, rules 89% | LLM 14, rules 5 of 80 | LLM 4, rules 2 of 17 | LLM 5, rules 4 | AI or rule reason; no human decision |

## Not measurable in this simulation

- **Speed to payment** (median and 90th percentile): the claims have no payment timeline, and the
  four-hour waits are an untested question (A1).
- **Reversals**: these happen up to 30 days after sorting.
- **Handler error under pace** for bulk sorting: modelled through the spotting-rate assumption,
  with one observed check from the bulk pilot (one person, 4 planted claims).
