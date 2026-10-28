# Stage 4b draft: suggestion screen (human draft)

Fill in each section. Short answers are fine. The AI reviews this before anything is built.

Constraint from the 4a gate: the AI may only route claims toward a human. It never clears a claim for payment.

## 1. What the handler sees

- When the AI flags a claim (closer look or suspicious): make sure the status is highly visbile, followed by the reason for the flag, supporting evidence and suggested next action. For needs a closer look, the handler needs to see what needs checking (e.g. missing documents, linked claims). For suspicious, the UI need to explain the specific risk reason or signal and recommend investigation. It's important that there's a clear visual distinction between claim facts (e.g. link claim 5 exist or policy A is effective as of 1/10/26) vs AI generated suggestions (e.g. the claim history of this claimant poses extra risk). Make it visually clear if information is missing.
- When the AI calls a claim simple (your flag idea): don't just show a green tick and "ready to pay". Instead show the suggested pile (simple - handler required), followed by a short 1-2 sentence explanaition of why the claim has been marked as simple. A reminder that the sorting suggestion is not a payout authorisation.
- Which claim facts are on the screen: Thinking of sections such as claim overview (claim ID, claimaint ID, amount, description), policy (policy number, effective date, policy status and date last checked), supporting evidence (required documents, missing documents and dates), related claims (linked claim IDs, status, linked claim descriptoion, and risk signals), workflow (approval required (yes / no), actions and current owner) and AI assessment (suggested pile, reason, supporting facts, missing information). 
- How the AI's reason is shown: A text box with a copy function so that reasons can be easily shared for compliance purposes. It needs to be a structured panel instead of free text. The structure should consist of the AI's sorting recommendation, reason, supporting evidence, whether further investigation is needed and a timestamp. 

## 2. What the handler can do

- Accept: confirm the suggested sorting pile
- Override (one-line reason is required): select a different and provide a 1-sentence reason for the override
- Anything else (for example, ask for information): the handler can view the linked claim, request missing information, escalate for review / approval.

## 3. The test

- Who plays the handler: work with 5-10 handlers, ideally with a range of experience (1 -10 years)
- Which claims, and how many: a mix of simple and more complex or suspicious claims (e.g. several linked claims or missing information). use the same difficulty mix across both the human and the AI assisted workflow, but different claims for each condition so that handlers don't just start applying learned patterns. Have a set of 60 claims for each workflow. 
- How claims are split between "with suggestion" and "without" (the same claim can't be seen twice by the same person): split evenly
- What is recorded (accept, override, time to decision, anything else): accept, override, time to decision, correct classification rate, explanatory reasons included (y/n)

## 4. A3b thresholds (locked at Stage 3, for reference)

- Pass: 30% or more of handler time saved, with override, reclassification and escalation rates no higher than without a suggestion.
- Fail: 10% or less saved, or any of those rates higher.

## 5. Anything you expect to see, or that would surprise you
- Handlers might over-trust an AI suggestion, and overlooking the supporting evidence provided by the AI
- A higher override rate might indicate that handlers are diligent in checkig AI output and supporting evidence / policy info
- I expect classifiaction errors to be higher in the AI generated version, as the AI might mot pick up on certain certain claim detail or nuance
- I would be surprised if the AI is more accurate in its sorting decisions than the human, given the level of expertise and context the handlers have
