"""Classifiers under test.

Every classifier returns, per transcript, a list of Flag(rule, evidence). The harness
only counts a flag if its evidence is a verbatim span of the transcript — no evidence,
no flag. That single rule removes a whole class of hallucinated flags from LLM output.

- KeywordClassifier: the over-flagging baseline (fires on topic words).
- EvidenceClassifier: v2 rules — coach-only, directive language, honours declines and
  referrals, and needs a member disclosure before judging escalation.
- ClaudeClassifier: LLM adapter (structured tool output + prompt caching). Optional;
  runs only when ANTHROPIC_API_KEY is set.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass

from harness.rules import RULES, RULE_IDS


@dataclass(frozen=True)
class Flag:
    rule: str
    evidence: str


def _coach_lines(turns):
    return [t["text"] for t in turns if t["speaker"] == "coach"]


def _member_lines(turns):
    return [t["text"] for t in turns if t["speaker"] == "member"]


def _first_match(pattern, lines):
    rx = re.compile(pattern, re.I)
    for line in lines:
        m = rx.search(line)
        if m:
            return line[m.start():m.end()]
    return None


class KeywordClassifier:
    """Baseline: flags whenever a topic word appears anywhere. High recall, poor precision."""
    name = "v1_keyword"
    PATTERNS = {
        "PFA": r"\b(fund|shares?|etf|invest\w*|super|card|loan|crypto)\b",
        "GUAR": r"\b(guarantee\w*|definitely|for sure|no question|will)\b",
        "TAX": r"\b(tax|claim|deduct\w*|declare)\b",
        "ESC": r"\b(stress\w*|anxious|worried|struggling|can't pay|can't afford|debt)\b",
    }

    def classify(self, turns):
        lines = [t["text"] for t in turns]
        out = []
        for rule, pat in self.PATTERNS.items():
            ev = _first_match(pat, lines)
            if ev:
                out.append(Flag(rule, ev))
        return out


class EvidenceClassifier:
    """v2: judge only what the coach says, require directive language, honour declines."""
    name = "v2_evidence"

    DECLINE = r"(can't recommend|licensed adviser|tax agent|lawyer|not something i can|nothing is guaranteed|can't promise)"
    # Verb is case-insensitive; the product/provider must be a capitalised name.
    PFA = (r"\b(?i:switch to|go with|put it into|get the|move (?:the money|your savings) into|"
           r"refinancing with|sell (?:them|it)|buy)\b[^.]*\b([A-Z][A-Za-z0-9]+)")
    GUAR = (r"(i guarantee|you will definitely|definitely, you'll|no question|for sure|"
            r"will definitely (?:get|save)|you'll definitely save|will be lower|will drop)")
    GUAR_OBJECT = r"\b(debt|approved|repayments?|deposit|save|rate|money|tax)\b|\$"
    TAX = (r"\b(claim (?:\d|the|your|67)|instant write-off|put it in (?:her|his) name|"
           r"don't need to declare|sacrifice \$)")
    HARDSHIP = (r"(can't pay|can't afford (?:food|rent|the|my|to)|missed .* repayments?|lost my job|skipping meals|"
                r"debt collectors|giving up|drowning|borrow from family|really stressed|"
                r"keeping me up|struggling to keep up)")
    SUPPORT = (r"(hardship|counsellor|lifeline|helpline|support line|follow-up|refer)")

    def classify(self, turns):
        coach = _coach_lines(turns)
        member = _member_lines(turns)
        out = []
        for line in coach:
            if re.search(self.DECLINE, line, re.I):
                continue
            m = re.search(self.PFA, line)
            if m:
                out.append(Flag("PFA", line[m.start():m.end()]))
                break
        for line in coach:
            m = re.search(self.GUAR, line, re.I)
            if m and re.search(self.GUAR_OBJECT, line, re.I) and not re.search(self.DECLINE, line, re.I):
                out.append(Flag("GUAR", line[m.start():m.end()]))
                break
        ev = _first_match(self.TAX, coach)
        if ev:
            out.append(Flag("TAX", ev))
        disclosure = _first_match(self.HARDSHIP, member)
        if disclosure and not _first_match(self.SUPPORT, coach):
            out.append(Flag("ESC", disclosure))
        return out


class ClaudeClassifier:
    """LLM classifier using the Anthropic Messages API.

    - Tool use forces structured output: {flags: [{rule, evidence}]}
    - The long, stable rule text sits in a system block marked for prompt caching,
      so repeated calls pay full price for it once.
    """
    name = "llm_claude"
    MODEL = os.environ.get("HARNESS_MODEL", "claude-sonnet-4-5")

    TOOL = {
        "name": "report_flags",
        "description": "Report compliance breaches found in the transcript.",
        "input_schema": {
            "type": "object",
            "properties": {"flags": {"type": "array", "items": {
                "type": "object",
                "properties": {
                    "rule": {"type": "string", "enum": RULE_IDS},
                    "evidence": {"type": "string", "description": "Exact quote from the transcript."},
                },
                "required": ["rule", "evidence"]}}},
            "required": ["flags"],
        },
    }

    def __init__(self):
        import anthropic  # optional dependency
        self.client = anthropic.Anthropic()
        self.system = [{
            "type": "text",
            "text": "You review financial-coaching transcripts for compliance. Flag a rule only "
                    "when the transcript clearly breaches it, and quote the exact evidence. "
                    "Respect the 'not a breach' cases.\n\n" + json.dumps(RULES, indent=2),
            "cache_control": {"type": "ephemeral"},
        }]

    def classify(self, turns):
        text = "\n".join(f"{t['speaker']}: {t['text']}" for t in turns)
        resp = self.client.messages.create(
            model=self.MODEL, max_tokens=512, system=self.system,
            tools=[self.TOOL], tool_choice={"type": "tool", "name": "report_flags"},
            messages=[{"role": "user", "content": text}],
        )
        block = next(b for b in resp.content if b.type == "tool_use")
        return [Flag(f["rule"], f["evidence"]) for f in block.input.get("flags", [])]


CLASSIFIERS = {c.name: c for c in (KeywordClassifier, EvidenceClassifier, ClaudeClassifier)}
