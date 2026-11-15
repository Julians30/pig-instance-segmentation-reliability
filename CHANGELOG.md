# Changelog

## 2026-11-15
- Zenodo version 1.0.0 published: DOI 10.5281/zenodo.24252738 (README badge, CITATION.cff and docs/ZENODO_ARCHIVE.md updated).
- Revised supplement ESM_1.pdf (lead text citing every table and figure; Eq. 1 reference; no numerical changes) and removed the journal name from the README status.
- Documented the prepared Zenodo source/supplement archive and reserved DOI, explicitly marked as unpublished pending authorization. Clarified the six deposit files and artifacts required for full reproduction.
- Notebook 54 completed (9/9 runs, each within 0.26–0.59% of the 60-min L4 budget).
- Added notebook **55**: Mask R-CNN with a time-based cosine learning-rate schedule (1e-4 to 1e-6), same budget and seeds; completed (3/3 runs).
- Added notebook **56**: single retrospective test evaluation of the 12 compute-matched checkpoints with the notebook-33 COCO protocol and a bridge check on the original seed-2026 checkpoints (differences ≤ 0.000121).
- New tables in `results/tables/` (`CERDOS_54_55_matched_budget_runs.csv`, `CERDOS_56_*.csv`), reports in `results/reports/` (`CERDOS_56_*`, prediction hash locks) and figures in `results/figures/`.
- README status updated to a neutral "manuscript in preparation"; `.zenodo.json` added for archiving; audit now expects 37 notebooks.

## 2026-11-14
- Notebook 54 version 3: the seed is selected automatically (first seed without the three `finish.json` files), so each session only needs «Run all»; fixed the YOLO mask-AP column name (`mAP50-95(M)`) in `finish.json`; the summary cell recovers the missing YOLO AP of seed 2026 from `results.csv` without editing the original records.
- Seed 2026 completed: YOLO11n-seg (223 epochs), YOLO26n-seg (136 epochs) and Mask R-CNN (26 epochs), 60.2–60.3 min each on one NVIDIA L4. Test set not evaluated.

## 2026-11-13
- Added complementary notebook **54** (`notebooks/07_complementary/`): equal NVIDIA L4 wall-clock training budget for YOLO11n-seg, YOLO26n-seg and Mask R-CNN ResNet50-FPN, seeds 2026–2028, same frozen date-disjoint split. Training and validation only; the test set is not evaluated.
- Version 2 of notebook 54 adds step 5b: one-time pre-caching of train/validation images and a Mask R-CNN timing re-measurement, because the first pilot read images directly from Google Drive.
- Status: timing pilot completed; budget-matched runs pending. No new results are reported.
- `scripts/audit_repository.py` now expects 35 clean notebooks; README, notebook index, reviewer guide and limitations updated accordingly.
