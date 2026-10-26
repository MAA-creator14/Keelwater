# Keelwater: claims sorting, AI-driven product lifecycle

A working record of how I'd approach the Keelwater sorting problem: what I'd test before committing a squad, how I'd use AI, and where I'd keep the decisions.

Keelwater is a fictional product. Every customer, quote, dataset and figure not in the brief is invented, and labelled as such.

## Start here

- `SKILL.md`: the lifecycle, its stages and gates.
- `aipdlc-log.md`: the gate decisions, one entry per stage, in order.
- `ai-use-log.md`: what I used AI for, what I kept, changed and rejected.
- `context/keelwater.md`: the brief's facts and the metric definitions.

## What is run and what is described

- **Run:** signal triage, failure map, assumptions register, a three-variant system test on 80 invented claims, a simulated suggestion screen, and the option comparison.
- **Described, with the gate written:** research beyond the brief, the spec, architecture, the build gate, and release and measurement.

## Reading order

1. `aipdlc-log.md`, to see the decisions and their order.
2. `work/04-prototype/`, for the test and the planted-fault check.
3. `ai-use-log.md`, for where I overrode or rejected the AI.

## Notes on the record

- Stage 0 instinct notes for stages 4a onward were rewritten after I'd seen AI suggestions. They're labelled "post-exposure" in the log.
- Commits follow the gate timestamps. Nothing has been backdated.
- Numbers are invented unless they're in the brief.
