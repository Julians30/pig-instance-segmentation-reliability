# Independent recalculation of COCO mask AP (Experiment 33)

## Audit status — 20 October 2026

**PASS.** Independently recomputed metrics from all **nine original archived prediction JSON files** and **373-image, 4,648-annotation** FaroPigSeg test ground truth. The test contains **five acquisition dates**. Comparisons to the saved Experiment 33 report:

- **Nine** mask-AP@[.50:.95], AP@.50 and AP@.75 global triplets = **27 scalar comparisons**.
- **45** run-by-date triplets (9 × 5) = **135 scalar comparisons**.
- **Total 162 metric comparisons**, maximum absolute difference **3.33e-16**, consistent with numerical rounding.
- **9 prediction file SHA-256 checks and 1 GT SHA-256 check** matched the frozen Experiment 33 provenance records.

This is a **separately authored NumPy implementation**, not a second call to the original analysis notebook and **not a run of the official `pycocotools` package**. It directly decodes COCO compressed RLE, computes exact mask intersections and unions, performs per-image confidence-ranked greedy assignment across IoU thresholds 0.50–0.95 (step 0.05), limits detections to 100 per image, and uses 101-point interpolated precision. **It does not retrain or rerun model inference.** The output can be independently regenerated provided the nine archived predictions and third-party dataset GT are available.

### Source files

- [Standalone audit script](../scripts/recompute_coco_masks_independent.py) (`numpy` is its sole runtime requirement).
- [Full independent numerical report](../results/reports/INDEPENDENT_COCO_AUDIT_RESULT.json): exact global values, maximal numerical discrepancies, and all nine prediction SHA-256 fingerprints.
- [Global comparison, machine-readable](../results/tables/INDEPENDENT_COCO_GLOBAL.csv).
- [Per-date comparison, machine-readable](../results/tables/INDEPENDENT_COCO_PER_DATE.csv).
- [Human-readable results](../results/reports/INDEPENDENT_COCO_AUDIT_SUMMARY.md).
- Original archived reference: [CERDOS_33_Informe_Final.json](../results/reports/CERDOS_33_Informe_Final.json).

### Command-line instructions

Install `numpy` in a suitable local Python environment (no CUDA or `pycocotools` required for this independent audit):

```bash
python -m pip install 'numpy>=1.24'
python scripts/recompute_coco_masks_independent.py --self-test
```

Fetch the FaroPigSeg ground-truth COCO JSON and the **nine saved prediction JSONs** from their original archival location **under their licensing/access conditions**. These masks and source images are not included here. The original notebook outputs are described in [REPRODUCIBILITY.md](REPRODUCIBILITY.md) and Notebook 33.

Create your *local, untracked* `prediction_map.json` with this format (actual filenames must be supplied by the user of the script):

```json
{
  "runs": [
    {"model": "YOLO11n-seg", "seed": 2026, "predictions": "predictions/YOLO11_seed2026.json"},
    {"model": "YOLO11n-seg", "seed": 2027, "predictions": "predictions/YOLO11_seed2027.json"},
    {"model": "YOLO11n-seg", "seed": 2028, "predictions": "predictions/YOLO11_seed2028.json"},
    {"model": "YOLO26n-seg", "seed": 2026, "predictions": "predictions/YOLO26_seed2026.json"},
    {"model": "YOLO26n-seg", "seed": 2027, "predictions": "predictions/YOLO26_seed2027.json"},
    {"model": "YOLO26n-seg", "seed": 2028, "predictions": "predictions/YOLO26_seed2028.json"},
    {"model": "Mask R-CNN", "seed": 2026, "predictions": "predictions/MaskRCNN_seed2026.json"},
    {"model": "Mask R-CNN", "seed": 2027, "predictions": "predictions/MaskRCNN_seed2027.json"},
    {"model": "Mask R-CNN", "seed": 2028, "predictions": "predictions/MaskRCNN_seed2028.json"}
  ]
}
```

Relative paths are resolved relative to `prediction_map.json`. Then run:

```bash
python scripts/recompute_coco_masks_independent.py \
  --ground-truth /path/to/CERDOS_09_GT_test_coco.json \
  --prediction-map /path/to/prediction_map.json \
  --reference results/reports/CERDOS_33_Informe_Final.json \
  --out outputs/independent_coco
```

The script writes `independent_coco_recomputed.json`, `independent_global.csv` and `independent_by_date.csv`. The report values are used **only for after-the-fact comparisons**; no saved numeric metrics are used as predicted mask outputs.

### Verification boundaries

- This independent output agrees with saved results to double-precision tolerance for the nine *existing* prediction sets. It does **not** prove model retraining can be reproduced on a fresh machine.
- Due to FaroPigSeg's upstream **CC BY-NC 4.0** terms, raw data and mask-label files are not relicensed or redistributed as MIT. Mask prediction JSONs remain in the original research archive; ask the corresponding author for lawful access when appropriate.
- This run is not an independently performed `pycocotools.COCOeval` execution. For a package-authoritative confirmation, `pycocotools` can be run using the same input files in an environment where it is installed.
- Five dates originate from **one farm/dataset**. There is no cross-farm external validation. The test split has been examined retrospectively in prior experiments.
- GitHub Actions verifies static repository integrity. No public workflow should imply that hidden-source COCO inputs are accessible to GitHub runners.
