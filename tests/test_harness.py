from harness.classifiers import EvidenceClassifier, Flag, KeywordClassifier
from harness.evaluate import grounded, load, score


def test_dataset_is_labelled_for_every_rule():
    items = load()
    assert len(items) >= 40
    for it in items:
        assert set(it["labels"]) == {"PFA", "GUAR", "TAX", "ESC"}


def test_flags_without_verbatim_evidence_are_dropped():
    turns = [{"speaker": "coach", "text": "Let's review your budget."}]
    kept, dropped = grounded([Flag("PFA", "buy Vanguard"), Flag("PFA", "review your budget")], turns)
    assert [f.evidence for f in kept] == ["review your budget"]
    assert len(dropped) == 1


def test_coach_decline_is_not_product_advice():
    turns = [{"speaker": "member", "text": "Which fund should I pick?"},
             {"speaker": "coach", "text": "I can't recommend a specific fund, a licensed adviser can."}]
    assert not [f for f in EvidenceClassifier().classify(turns) if f.rule == "PFA"]


def test_referral_clears_escalation():
    turns = [{"speaker": "member", "text": "I can't pay rent this month."},
             {"speaker": "coach", "text": "I can connect you with a financial counsellor today."}]
    assert not [f for f in EvidenceClassifier().classify(turns) if f.rule == "ESC"]


def test_v2_cuts_false_flags_without_losing_recall():
    items = load()
    v1, v2 = score(KeywordClassifier(), items), score(EvidenceClassifier(), items)
    assert v2["overall"]["fp"] < v1["overall"]["fp"]
    for rule in v1["per_rule"]:
        assert v2["per_rule"][rule]["recall"] >= v1["per_rule"][rule]["recall"]
