"""The three Stage 4a sorting variants. Each takes one claim dict and returns
{"pile": ..., "reason": ..., "cited_facts": [{"field": ..., "value": ...}]}.

All three are stand-ins built for a simulation on invented claims:
  rules      written by the AI, which also wrote the claims (a known bias).
  prototype  a naive Bayes model on invented older claims, using only line, amount
             band and missing documents, to mimic a model 18 months out of date.
             It gives no reason, as the old prototype didn't.
  llm        a real model call, which sees only the claim record.
"""

import json
import math
import os
from collections import Counter, defaultdict
from datetime import date

PILES = ["simple", "closer_look", "suspicious"]
STALE_DAYS = 60


def _days(a, b):
    return (date.fromisoformat(a) - date.fromisoformat(b)).days


def _missing_docs(claim):
    return [k for k, v in claim["documents"].items() if v is False]


# --- Rules baseline -----------------------------------------------------------

def rules(claim):
    facts = []

    def cite(field, value):
        facts.append({"field": field, "value": str(value)})

    text = claim["description"].lower()
    policy_age = _days(claim["incident_date"], claim["policy_start_date"])
    history = claim["claimant_history"]
    recent = [h for h in history if _days(claim["received_at"], h["date"]) <= 365]

    if policy_age < 30:
        cite("policy_start_date", claim["policy_start_date"])
        return _out("suspicious", f"Policy started {policy_age} days before the incident.", facts)
    if len(recent) >= 3:
        for h in recent:
            cite("claimant_history", h["claim_id"])
        return _out("suspicious", f"Claimant has {len(recent)} claims in the last 12 months.",
                    facts)
    if "cash" in text:
        cite("description", "cash")
        return _out("suspicious", "Claimant asks for payment in cash.", facts)
    if "dated" in text and "before" in text:
        cite("description", "dated")
        return _out("suspicious", "Supporting document is dated before the incident.", facts)

    reasons = []
    if not claim["policy_number"]:
        cite("policy_number", "None")
        reasons.append("no policy number")
    missing = _missing_docs(claim)
    if missing:
        for m in missing:
            cite("documents", m)
        reasons.append(f"missing {', '.join(missing)}")
    if claim["related_claims"]:
        ids = ", ".join(r["claim_id"] for r in claim["related_claims"])
        cite("related_claims", ids)
        reasons.append(f"related to {ids}")
    if recent:
        for h in recent:
            cite("claimant_history", h["claim_id"])
        reasons.append("claimant has claimed in the last 12 months")
    stale = _days(claim["received_at"], claim["policy_status_checked_at"])
    if stale > STALE_DAYS:
        cite("policy_status_checked_at", claim["policy_status_checked_at"])
        reasons.append(f"policy status last checked {stale} days ago")
    if "liability not yet confirmed" in text:
        cite("description", "liability not yet confirmed")
        reasons.append("third-party liability not confirmed")
    if reasons:
        return _out("closer_look", "Closer look: " + "; ".join(reasons) + ".", facts)

    cite("amount_gbp", claim["amount_gbp"])
    return _out("simple", f"Complete claim, no history or links, £{claim['amount_gbp']:,}.", facts)


def _out(pile, reason, facts):
    return {"pile": pile, "reason": reason, "cited_facts": facts}


# --- Old-prototype stand-in ---------------------------------------------------

def _band(amount):
    return "low" if amount < 500 else "mid" if amount < 3000 else "high"


class Prototype:
    def __init__(self, history_path="history.json"):
        rows = json.load(open(history_path))
        self.prior = Counter(r["pile"] for r in rows)
        self.cond = defaultdict(Counter)
        for r in rows:
            for f, v in self._features(r["line"], r["amount_gbp"], r["docs_missing"]):
                self.cond[(f, v)][r["pile"]] += 1
        self.n = len(rows)

    @staticmethod
    def _features(line, amount, docs_missing):
        return [("line", line), ("band", _band(amount)), ("docs_missing", docs_missing)]

    def __call__(self, claim):
        feats = self._features(claim["line"], claim["amount_gbp"], bool(_missing_docs(claim)))
        scores = {}
        for p in PILES:
            s = math.log((self.prior[p] + 1) / (self.n + 3))
            for fv in feats:
                s += math.log((self.cond[fv][p] + 1) / (self.prior[p] + 2))
            scores[p] = s
        pile = max(scores, key=scores.get)
        return {"pile": pile, "reason": "", "cited_facts": []}


# --- LLM classifier -----------------------------------------------------------

LLM_MODEL = "claude-opus-5-5"

SYSTEM = """You sort new insurance claims for a claims handler. Put each claim in one pile:
- simple: pay it quickly.
- closer_look: check the details first.
- suspicious: send it for investigation.

Give a short reason a customer or regulator could follow. Cite only facts that appear in the
claim record, naming the field each fact comes from. If information needed to decide is
missing, say so rather than assuming it."""

SCHEMA = {
    "type": "object",
    "properties": {
        "pile": {"type": "string", "enum": PILES},
        "reason": {"type": "string"},
        "cited_facts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"field": {"type": "string"}, "value": {"type": "string"}},
                "required": ["field", "value"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["pile", "reason", "cited_facts"],
    "additionalProperties": False,
}


class LLM:
    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic()

    def __call__(self, claim):
        record = {k: v for k, v in claim.items() if k != "id"}
        response = self.client.beta.messages.create(
            model=LLM_MODEL,
            max_tokens=8000,
            system=SYSTEM,
            betas=["server-side-fallback-2026-07-01"],
            extra_body={"fallbacks": "default"},
            output_config={"effort": "medium",
                           "format": {"type": "json_schema", "schema": SCHEMA}},
            messages=[{"role": "user",
                       "content": "Claim record:\n" + json.dumps(record, indent=1)}],
        )
        if response.stop_reason == "refusal":
            return {"pile": "refused", "reason": "", "cited_facts": [], "model": response.model}
        text = next((b.text for b in response.content if b.type == "text"), None)
        if response.stop_reason == "max_tokens" or text is None:
            return {"pile": "no_answer", "reason": "", "cited_facts": [], "model": response.model}
        out = json.loads(text)
        out["model"] = response.model
        return out


def load_env(path=".env"):
    """Read KEY=value lines from a git-ignored .env file into the environment."""
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"'))
