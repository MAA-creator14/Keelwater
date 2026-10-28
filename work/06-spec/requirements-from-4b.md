# Requirements carried from Stage 4b

Raised by the human at the Stage 4b gate on 28 Oct 2026, for the Stage 6 spec.

1. **A reason on every decision.** Every sorting decision records a reason a customer or regulator could follow. When a handler accepts an AI suggestion, the AI's reason is recorded as adopted by that handler, with their name and the time. An override needs the handler's own one-line reason. (The 4b mock made reasons optional on claims without a suggestion, which doesn't meet the brief's explainability requirement.)
2. **A similar-claims check.** The screen shows claims with similar descriptions, amounts, dates or vehicles as record facts, so a handler can rule out duplicates. The AI sees one claim at a time and can't do this itself (Failure 4, missing context). In the 4b pilot, the handler suspected duplicates on 7 claims and had no way to check.
