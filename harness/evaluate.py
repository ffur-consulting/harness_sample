"""Score a classifier against the labelled set.

    python -m harness.evaluate --classifier v1_keyword --split dev
    python -m harness.evaluate --classifier v2_evidence --split holdout
    python -m harness.compare reports/v1_keyword_holdout.json reports/v2_evidence_holdout.json

Writes reports/<classifier>.json (metrics + every error with its evidence) and
reports/<classifier>.md (human-readable).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from harness.classifiers import CLASSIFIERS
from harness.rules import RULE_IDS, RULES

ROOT = Path(__file__).resolve().parents[1]


def load(path=ROOT / "data" / "transcripts.jsonl"):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def transcript_text(turns):
    return "\n".join(t["text"] for t in turns)


def grounded(flags, turns):
    """Keep only flags whose evidence is a verbatim span of the transcript."""
    text = transcript_text(turns)
    kept, dropped = [], []
    for f in flags:
        (kept if f.evidence and f.evidence in text else dropped).append(f)
    return kept, dropped


def score(classifier, items):
    counts = {r: {"tp": 0, "fp": 0, "fn": 0, "tn": 0} for r in RULE_IDS}
    errors, ungrounded = [], 0
    for it in items:
        kept, dropped = grounded(classifier.classify(it["turns"]), it["turns"])
        ungrounded += len(dropped)
        predicted = {f.rule: f.evidence for f in kept}
        for r in RULE_IDS:
            gold, pred = it["labels"][r] == 1, r in predicted
            key = {(True, True): "tp", (False, True): "fp",
                   (True, False): "fn", (False, False): "tn"}[(gold, pred)]
            counts[r][key] += 1
            if key in ("fp", "fn"):
                errors.append({"id": it["id"], "rule": r, "type": key,
                               "evidence": predicted.get(r), "why_label": it["why"]})
    per_rule = {}
    for r, c in counts.items():
        p = c["tp"] / (c["tp"] + c["fp"]) if c["tp"] + c["fp"] else 1.0
        rec = c["tp"] / (c["tp"] + c["fn"]) if c["tp"] + c["fn"] else 1.0
        f1 = 2 * p * rec / (p + rec) if p + rec else 0.0
        per_rule[r] = {**c, "precision": round(p, 3), "recall": round(rec, 3), "f1": round(f1, 3)}
    tot = {k: sum(c[k] for c in counts.values()) for k in ("tp", "fp", "fn", "tn")}
    micro_p = tot["tp"] / (tot["tp"] + tot["fp"]) if tot["tp"] + tot["fp"] else 1.0
    micro_r = tot["tp"] / (tot["tp"] + tot["fn"]) if tot["tp"] + tot["fn"] else 1.0
    return {
        "classifier": classifier.name, "n_transcripts": len(items),
        "per_rule": per_rule,
        "overall": {**tot, "precision": round(micro_p, 3), "recall": round(micro_r, 3),
                    "false_positive_rate": round(tot["fp"] / (tot["fp"] + tot["tn"]), 3)},
        "ungrounded_flags_dropped": ungrounded,
        "errors": errors,
    }


def to_markdown(rep):
    lines = [f"# {rep['classifier']} — {rep['n_transcripts']} labelled transcripts", "",
             "| Rule | Precision | Recall | F1 | FP | FN |", "|---|---|---|---|---|---|"]
    for r, m in rep["per_rule"].items():
        lines.append(f"| {r} ({RULES[r]['name']}) | {m['precision']:.2f} | {m['recall']:.2f} | "
                     f"{m['f1']:.2f} | {m['fp']} | {m['fn']} |")
    o = rep["overall"]
    lines += ["", f"**Overall:** precision {o['precision']:.2f}, recall {o['recall']:.2f}, "
                  f"false-positive rate {o['false_positive_rate']:.2f} "
                  f"({o['fp']} false flags). Ungrounded flags dropped: {rep['ungrounded_flags_dropped']}.",
              "", "## Errors", "", "| id | rule | type | evidence | label note |", "|---|---|---|---|---|"]
    for e in rep["errors"]:
        lines.append(f"| {e['id']} | {e['rule']} | {e['type']} | {e['evidence'] or ''} | {e['why_label']} |")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--classifier", required=True, choices=list(CLASSIFIERS))
    ap.add_argument("--split", default="dev", choices=["dev", "holdout"],
                    help="dev = transcripts.jsonl (used for tuning); holdout = never tuned on")
    args = ap.parse_args()
    path = ROOT / "data" / ("transcripts.jsonl" if args.split == "dev" else "holdout.jsonl")
    rep = score(CLASSIFIERS[args.classifier](), load(path))
    rep["classifier"] = f"{rep['classifier']}_{args.split}"
    out = ROOT / "reports"
    out.mkdir(exist_ok=True)
    (out / f"{rep['classifier']}.json").write_text(json.dumps(rep, indent=2))
    (out / f"{rep['classifier']}.md").write_text(to_markdown(rep))
    o = rep["overall"]
    print(f"{rep['classifier']}: precision={o['precision']} recall={o['recall']} "
          f"false_flags={o['fp']} -> reports/{rep['classifier']}.md")


if __name__ == "__main__":
    main()
