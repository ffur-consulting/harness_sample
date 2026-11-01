# v2_evidence_holdout — 16 labelled transcripts

| Rule | Precision | Recall | F1 | FP | FN |
|---|---|---|---|---|---|
| PFA (Personal financial product advice) | 1.00 | 0.50 | 0.67 | 0 | 1 |
| GUAR (Guaranteed outcome) | 1.00 | 0.50 | 0.67 | 0 | 1 |
| TAX (Specific tax or legal advice) | 1.00 | 0.50 | 0.67 | 0 | 1 |
| ESC (Vulnerability not escalated) | 1.00 | 0.00 | 0.00 | 0 | 2 |

**Overall:** precision 1.00, recall 0.38, false-positive rate 0.00 (0 false flags). Ungrounded flags dropped: 0.

## Errors

| id | rule | type | evidence | label note |
|---|---|---|---|---|
| h02 | PFA | fn |  | Named provider recommendation. |
| h04 | GUAR | fn |  | Product rec + certainty. |
| h09 | ESC | fn |  | Hardship (behind on bills), no referral. |
| h12 | ESC | fn |  | Serious vulnerability, no referral. |
| h15 | TAX | fn |  | Specific (and harmful) tax statement. |
