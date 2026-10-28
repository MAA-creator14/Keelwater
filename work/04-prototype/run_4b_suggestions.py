"""Stage 4b: pick the pilot claims and get structured AI suggestions for the 12 shown with one.

Simulation on invented claims. Claims were picked from those not yet discussed with the
human, as two halves matched on correct pile (5 simple, 6 closer look, 1 suspicious each).
The "with suggestion" half includes three claims the 4a LLM wrongly sorted as simple,
to test whether a handler accepts a wrong suggestion.

Usage: python3 run_4b_suggestions.py   (needs ANTHROPIC_API_KEY in .env; 12 API calls)
Writes 4b-pilot-set.json and 4b-suggestions.json.
"""

import json
from datetime import datetime, timezone

import anthropic

from variants import LLM_MODEL, PILES, SYSTEM, load_env

WITH = ["K035", "K065", "K067", "K005", "K022", "K002", "K007", "K017", "K025", "K010",
        "K020", "K063"]
WITHOUT = ["K069", "K026", "K032", "K042", "K049", "K050", "K027", "K028", "K029", "K037",
           "K023", "K021"]

SYSTEM_4B = SYSTEM + """

Also say what information is missing from the record, whether the claim needs investigation,
and the next action a handler should take. A suggestion is never a payment authorisation."""

SCHEMA_4B = {
    "type": "object",
    "properties": {
        "pile": {"type": "string", "enum": PILES},
        "reason": {"type": "string"},
        "supporting_facts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"field": {"type": "string"}, "value": {"type": "string"}},
                "required": ["field", "value"],
                "additionalProperties": False,
            },
        },
        "missing_information": {"type": "array", "items": {"type": "string"}},
        "investigation_needed": {"type": "boolean"},
        "next_action": {"type": "string"},
    },
    "required": ["pile", "reason", "supporting_facts", "missing_information",
                 "investigation_needed", "next_action"],
    "additionalProperties": False,
}


def suggest(client, claim):
    record = {k: v for k, v in claim.items() if k != "id"}
    response = client.beta.messages.create(
        model=LLM_MODEL,
        max_tokens=8000,
        system=SYSTEM_4B,
        betas=["server-side-fallback-2026-07-01"],
        extra_body={"fallbacks": "default"},
        output_config={"effort": "medium",
                       "format": {"type": "json_schema", "schema": SCHEMA_4B}},
        messages=[{"role": "user", "content": "Claim record:\n" + json.dumps(record, indent=1)}],
    )
    text = next((b.text for b in response.content if b.type == "text"), None)
    if response.stop_reason in ("refusal", "max_tokens") or text is None:
        return {"pile": "no_answer", "stop_reason": response.stop_reason, "model": response.model}
    out = json.loads(text)
    out["model"] = response.model
    out["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out["usage"] = {"input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens}
    return out


def main():
    claims = {c["id"]: c for c in json.load(open("claims.json"))}
    json.dump({"with_suggestion": WITH, "without_suggestion": WITHOUT},
              open("4b-pilot-set.json", "w"), indent=1)
    load_env()
    client = anthropic.Anthropic()
    out = {}
    for i in WITH:
        out[i] = suggest(client, claims[i])
        print(i, out[i]["pile"])
    json.dump(out, open("4b-suggestions.json", "w"), indent=1)


if __name__ == "__main__":
    main()
