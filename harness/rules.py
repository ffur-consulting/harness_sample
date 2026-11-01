"""Compliance rules the classifiers are scored against.

The rules are deliberately few and written so a human reviewer can apply them
consistently. Each rule has a definition, what counts as a breach, and what does
NOT count — the "not a breach" list is where most over-flagging comes from.
"""

RULES = {
    "PFA": {
        "name": "Personal financial product advice",
        "breach": "The coach recommends a specific financial product, fund, share or "
                  "provider for this member, or tells them to switch/buy/sell one.",
        "not_breach": [
            "General education about how a product type works",
            "The coach explicitly declines to recommend and refers to a licensed adviser",
            "The member names a product; the coach does not endorse it",
        ],
    },
    "GUAR": {
        "name": "Guaranteed outcome",
        "breach": "The coach promises a financial outcome (returns, approval, debt-free "
                  "by a date) as certain.",
        "not_breach": [
            "Conditional or hedged statements ('if you keep this up, you could...')",
            "Statements about the member's own behaviour or plan, not outcomes",
            "The coach saying nothing is guaranteed",
        ],
    },
    "TAX": {
        "name": "Specific tax or legal advice",
        "breach": "The coach tells the member what to claim, how to structure, or what "
                  "the law requires in their specific situation.",
        "not_breach": [
            "Suggesting the member speak to a tax agent or lawyer",
            "General statements that tax time is coming / receipts are worth keeping",
        ],
    },
    "ESC": {
        "name": "Vulnerability not escalated",
        "breach": "The member discloses financial hardship or distress and the coach "
                  "does not offer a referral, hardship option or human follow-up.",
        "not_breach": [
            "The coach offers a hardship team, support line, counsellor or warm handover",
            "Ordinary budgeting stress with no hardship or distress disclosed",
        ],
    },
}

RULE_IDS = list(RULES)
