"""Compare two runs and act as a release gate.

    python -m harness.compare reports/v1_keyword.json reports/v2_evidence.json

Exit code 1 if the candidate loses recall on ANY rule versus the baseline: cutting
false positives is only a win if real breaches are still caught.
"""
import json
import sys

from harness.rules import RULE_IDS


def main(base_path, cand_path):
    base, cand = (json.load(open(p)) for p in (base_path, cand_path))
    print(f"{'rule':<6}{'precision':>22}{'recall':>22}{'false flags':>16}")
    regressions = []
    for r in RULE_IDS:
        b, c = base["per_rule"][r], cand["per_rule"][r]
        print(f"{r:<6}{b['precision']:>10.2f} -> {c['precision']:<9.2f}"
              f"{b['recall']:>10.2f} -> {c['recall']:<9.2f}{b['fp']:>7} -> {c['fp']}")
        if c["recall"] < b["recall"]:
            regressions.append(r)
    bo, co = base["overall"], cand["overall"]
    print(f"\noverall false flags {bo['fp']} -> {co['fp']}, "
          f"precision {bo['precision']:.2f} -> {co['precision']:.2f}, "
          f"recall {bo['recall']:.2f} -> {co['recall']:.2f}")
    if regressions:
        print(f"GATE FAILED: recall dropped on {', '.join(regressions)}")
        return 1
    print("GATE PASSED: no rule lost recall")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
