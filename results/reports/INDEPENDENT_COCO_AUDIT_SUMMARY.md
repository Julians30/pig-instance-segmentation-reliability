# Independent COCO mask AP recalculation — complete audit

**Status: PASS — 9 global evaluations and 45 acquisition-date evaluations match the frozen experiment-33 report.**

The audit operated on the original 373-image / 4,648-object compressed-RLE COCO test ground truth and the nine saved prediction JSONs (three models × three training seeds). A separate, dependency-light NumPy implementation decoded RLE interval runs, calculated exact mask intersections/unions, used confidence-ranked greedy one-to-one matches at IoU 0.50 through 0.95 (increments 0.05), capped predictions at 100 per image, and evaluated 101 recall thresholds. The archived AP outputs were used **only as reference values for the final comparison**, not as evaluator inputs.

| Configuration | Seed | AP@[.50:.95] | AP@.50 | AP@.75 | Absolute delta max |
|---|---:|---:|---:|---:|---:|
| YOLO11n-seg | 2026 | 0.865452749 | 0.927965571 | 0.923790459 | 1.11e-16 |
| YOLO11n-seg | 2027 | 0.860989664 | 0.924765783 | 0.919546945 | 1.11e-16 |
| YOLO11n-seg | 2028 | 0.863466174 | 0.926856094 | 0.923064944 | 0.00e+00 |
| YOLO26n-seg | 2026 | 0.849508402 | 0.915124113 | 0.908381095 | 0.00e+00 |
| YOLO26n-seg | 2027 | 0.850028817 | 0.915331966 | 0.908127157 | 1.11e-16 |
| YOLO26n-seg | 2028 | 0.842542459 | 0.914530164 | 0.906514728 | 0.00e+00 |
| Mask R-CNN | 2026 | 0.796153380 | 0.919159795 | 0.881156895 | 0.00e+00 |
| Mask R-CNN | 2027 | 0.797614686 | 0.909323076 | 0.876032713 | 1.11e-16 |
| Mask R-CNN | 2028 | 0.790434873 | 0.903190499 | 0.868510187 | 0.00e+00 |

**Summary:** 27 global metrics and 135 date-specific metrics checked (162 scalar comparisons). Maximum absolute discrepancy: **3.33e-16**.

**Scope:** This is a second, independently written evaluator for the *same frozen prediction JSON files*, not new model inference, a from-scratch training rerun, or independent-farm validation. It is not an execution of the official `pycocotools` package; an additional package-authoritative cross-check can be run where `pycocotools` is installed. Confidence, mask threshold and assignment criteria are those already represented by the archived predicted masks and scores.

**Verification:** Source input SHA-256 hashes are saved in `INDEPENDENT_COCO_AUDIT_RESULT.json`. The complete predicted masks and third-party COCO ground truth are not redistributed in the public repository because of upstream data-license considerations.

**Reproduce:** Use the Python source `scripts/recompute_coco_masks_independent.py` with a local input map and `python -m pip install numpy`. The full input map and instructions appear in `docs/INDEPENDENT_COCO_AUDIT.md`.
