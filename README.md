# Pig instance segmentation reliability: a multidimensional assessment

[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](LICENSE)
[![Dataset: CC BY-NC 4.0](https://img.shields.io/badge/Upstream%20Data-CC%20BY--NC%204.0-lightgrey.svg)](DATA_LICENSE.md)
[![Repository integrity](https://github.com/Julians30/pig-instance-segmentation-reliability/actions/workflows/repository-audit.yml/badge.svg)](.github/workflows/repository-audit.yml)
[![Status](https://img.shields.io/badge/Status-Manuscript%20in%20preparation-2E6DA4)](#)

**Research code and documented experimental artifacts** for the manuscript *Selecting pig instance segmentation models for farm monitoring: compute-matched and date-disjoint evidence from YOLO11, YOLO26 and Mask R-CNN*. The manuscript is **not yet accepted or published**.

**Researchers:** Julián Coronel-Reyes and Alexander Haro-Sarango. The repository includes **37 clean Colab notebooks** (numbered 00–33, notebook 25 being the corrected version, plus the complementary compute-matched notebooks **54–56**), frozen date-disjoint split manifests, records of the nine-seed COCO assessment, manuscript-oriented figures and automated integrity checks.

## Research question and experimental scope

What do three pig instance-segmentation **training configurations** reveal about accuracy and reliability beyond a single mask AP score? We compare **YOLO11n-seg**, **YOLO26n-seg**, and **Mask R-CNN ResNet50-FPN**, each trained with seeds **2026, 2027 and 2028**. We examine date-wise segmentation performance, geometry, counting thresholds, probabilistic calibration, efficiency and exploratory Grad-CAM maps.

**Key design limitations:** in the original recipes, training budgets differ by architecture (YOLO up to 60 epochs, batch 8; Mask R-CNN 12 epochs, batch 1); notebooks 54–56 add an equal-training-time sensitivity analysis (below). The date-disjoint test is from the **same dataset/farm**, was consulted in earlier analyses, and **is not external-farm validation**. Differences are descriptive; three seeds are not nine independent test sessions. Calibration and the counting operating-point analyses originated from the 2026 configurations and are not asserted to cover all nine runs.

## Complementary experiments 54–56: equal L4 training-time budget (completed)

The original recipes use different training budgets per architecture. Three complementary notebooks test whether the ranking is an artefact of those budgets:

- [`54`](notebooks/07_complementary/54_CERDOS_Presupuesto_Equiparado_L4_GPU.ipynb) retrains YOLO11n-seg, YOLO26n-seg and Mask R-CNN ResNet50-FPN with a **common 60-min wall-clock training budget on one NVIDIA L4 GPU**, seeds 2026–2028, same frozen split and SHA-256-verified inputs (train/validation only).
- [`55`](notebooks/07_complementary/55_CERDOS_MaskRCNN_LR_Coseno_L4_GPU.ipynb) repeats the Mask R-CNN runs with a **time-based cosine learning-rate schedule** (1e-4 to 1e-6), same budget and seeds (train/validation only).
- [`56`](notebooks/07_complementary/56_CERDOS_Evaluacion_Test_Presupuesto_Equiparado_GPU.ipynb) evaluates the 12 best-validation checkpoints **once** on the test set with the same COCO protocol as notebook 33, plus a bridge check that re-infers the three original seed-2026 checkpoints. This is a **retrospective** evaluation: the test set was consulted in earlier analyses.

| Configuration (equal 60-min budget) | Epochs per seed | Best validation mask AP | **Test mask AP** (mean ± SD) | Original recipe (test) |
|---|---|---:|---:|---:|
| YOLO11n-seg | 223 / 229 / 228 | 0.8770 ± 0.0023 | **0.8550 ± 0.0033** | 0.8633 |
| YOLO26n-seg | 136 / 139 / 136 | 0.8654 ± 0.0013 | **0.8481 ± 0.0045** | 0.8474 |
| Mask R-CNN, constant LR | 26 / 27 / 26 | 0.8203 ± 0.0022 | **0.8025 ± 0.0090** | 0.7947 |
| Mask R-CNN, cosine LR | 27 / 27 / 27 | 0.8311 ± 0.0036 | **0.8052 ± 0.0029** | 0.7947 |

- The ordering YOLO11n-seg > YOLO26n-seg > Mask R-CNN held for every seed; the YOLO11n-seg − Mask R-CNN (cosine) test gap was 4.99 points (6.86 with the original recipes).
- YOLO11n-seg lost 0.83 test points despite higher validation AP; the cosine schedule improved validation AP by 1.08 points but test AP by only 0.27 points (mixed signs across seeds).
- Bridge check: the original seed-2026 checkpoints reproduced their archived test AP within 0.000121.
- Equal wall-clock time is **not** equal FLOPs, energy or identical recipes (augmentation, input sizes and optimizers still differ). Tables: [`results/tables/CERDOS_54_55_matched_budget_runs.csv`](results/tables/CERDOS_54_55_matched_budget_runs.csv), [`CERDOS_56_test_global.csv`](results/tables/CERDOS_56_test_global.csv), [`CERDOS_56_test_per_date.csv`](results/tables/CERDOS_56_test_per_date.csv), [`CERDOS_56_bridge_check.csv`](results/tables/CERDOS_56_bridge_check.csv).

## Dataset and frozen split

| Split | Images | Acquisition dates |
|---|---:|---:|
| Training | 949 | 16 |
| Validation | 196 | 4 |
| Test | 373 | 5 |
| **Total** | **1,518** | **25** |

The raw images and labels are **not** in this repository. Obtain FaroPigSeg from [its authors](https://github.com/yudong888/FaroPig-Datasets/tree/main/FaroPigSeg) subject to **CC BY-NC 4.0**, then read [data/README.md](data/README.md). Split files in [`data/partitions/`](data/partitions/) are the **unaltered author originals**; their Google Drive absolute prefixes must be **rebased** on another machine by [`scripts/rebase_split_lists.py`](scripts/rebase_split_lists.py). The fact that an image appears under the upstream `test/images` physical folder **does not** mean it belongs to our date-disjoint test; **use the manifest assignments**.

## Main test results (COCO mask AP@[.50:.95])

| Trained configuration | Mean over three seeds | Sample SD | Evaluation images |
|---|---:|---:|---:|
| YOLO11n-seg | **0.8633** | 0.0022 | 373 |
| YOLO26n-seg | **0.8474** | 0.0042 | 373 |
| Mask R-CNN ResNet50-FPN | **0.7947** | 0.0038 | 373 |

The full-precision **nine-run** data, **45 run–date** values, frozen evaluation protocol and checkpoint/prediction SHA-256 records are in [`results/`](results/README.md). Summaries are **recorded outputs**, not evidence of an independent repeat run on GitHub Actions.

## Independent COCO numerical audit

**Verified on the nine archived prediction JSON files:** a separately authored compressed-RLE mask evaluator recalculated 9 global × 3 metrics and 45 date-level × 3 metrics. All **162** scalar comparisons reproduce Experiment 33 at floating-point precision (maximum absolute difference **3.33 × 10⁻¹⁶**). The exact source, per-date/global records, input SHA-256 fingerprints and instructions are documented in [Independent COCO audit](docs/INDEPENDENT_COCO_AUDIT.md). This is a **separate implementation over the same predictions**, not new training, new model inference or a run of the official `pycocotools` library. The raw predictions/GT are not all hosted in this repository.

## Reviewers: evidence map

Start with the [reviewer quick-start and claim-to-artifact guide](docs/REVIEWER_GUIDE.md), which distinguishes static repository checks from independent COCO recomputation and gives a direct path from the manuscript's claims to the numbered notebooks and artifacts.

## Navigation

| Folder | Purpose |
|---|---|
| [`notebooks/01_data`](notebooks/01_data) | Download, audit and date-disjoint split construction (00–02) |
| [`notebooks/02_training`](notebooks/02_training) | Original and repeated YOLO11, YOLO26 and Mask R-CNN training (03, 06, 22, 31, 32) |
| [`notebooks/03_evaluation`](notebooks/03_evaluation) | Segmentation, COCO, acquisition dates, geometry, efficiency and nine-seed comparison (04–12, 17–19, 23, 33) |
| [`notebooks/04_calibration`](notebooks/04_calibration) | Candidate detections, Platt calibration and confidence sensitivity (13–16, 21) |
| [`notebooks/05_diagnostics`](notebooks/05_diagnostics) | Count-error diagnostics, validation-only threshold selection and case reviews (24–30) |
| [`notebooks/06_explainability`](notebooks/06_explainability) | Same-instance Grad-CAM visualizations (20; qualitative only) |
| [`notebooks/07_complementary`](notebooks/07_complementary) | Equal L4 training-time budget (54), cosine-LR Mask R-CNN control (55) and single retrospective test evaluation (56) |
| [`data/partitions`](data/partitions) | Frozen split files and date manifest (no images/labels) |
| [`results/`](results/README.md) | Original small JSON reports, Excel summaries, CSV exports and publication figures |
| [`scripts/`](scripts) | Dependency-free split rebasing and integrity tests |
| [`docs/`](docs/REPRODUCIBILITY.md) | Reproduction order, notebook mapping, experimental limitations and provenance |

## Reproduction: start here

1. Read [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) and [`docs/NOTEBOOK_INDEX.md`](docs/NOTEBOOK_INDEX.md).
2. Download and extract FaroPigSeg from the official source. **Do not use the upstream random split instead of the frozen date split.**
3. Run `python scripts/rebase_split_lists.py --dataset-root /path/to/FaroPigSeg --out-dir outputs/local_split --strict` to regenerate local absolute lists and YAML. `--strict` needs all original image files present.
4. Use a CUDA-enabled Google Colab environment with versions recorded in [`environment/README.md`](environment/README.md), and adapt the notebooks' project root paths when running outside the original Drive.
5. For a **from-scratch** reconstruction follow 00–03/06/22, then 31/32, then COCO evaluations 09, 23 and **33**; existing historical predictions/weights are otherwise expected by notebook 33. Calibration and counting notebooks are an **additional** branch of the analysis.
6. Run `python scripts/audit_repository.py` for local **static/provenance** verification. The GitHub Actions check runs this automatically but **does not run training or COCO evaluation**.

## What is independently verified here?

The code publication contains notebook source cells with executed outputs stripped, split files copied byte-for-byte, original small experiment reports, nine-seed summaries and self-checks for counts/date separation/checksums. It does **not** ship model weights, the FaroPigSeg images, ground-truth masks, or a fully containerized end-to-end GPU reproduction. A separate numerical recomputation of archived masks **has** now been completed and published as summary evidence. The original Colab notebooks also include environment-specific paths; details and remaining items are maintained in [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md).

## Versioned archive

A version 1.0.0 Zenodo deposit has been prepared with the full source snapshot, integrity manifests and supplementary tables S1–S17 / figures S1–S4. **Reserved DOI: `10.5281/zenodo.24252738`; publication is pending and the DOI is not yet registered.** See [archive contents and availability](docs/ZENODO_ARCHIVE.md). This is a software/artifact archive; the associated manuscript is in preparation and not yet accepted or published.

## Code/data availability, citation and licenses

- Project code/documentation: **MIT**, [`LICENSE`](LICENSE). The MIT license does **not** supersede third-party data or model licenses.
- Original FaroPigSeg data: **CC BY-NC 4.0**. See [`DATA_LICENSE.md`](DATA_LICENSE.md).
- Please cite the upstream FaroPigSeg article: *Housed Pig Identification and Tracking for Precision Livestock Farming*, *Expert Systems with Applications*, 293 (2025), 128466, https://doi.org/10.1016/j.eswa.2025.128466.
- Software citation metadata: [`CITATION.cff`](CITATION.cff); no DOI or publication status is invented for the present study.

For scientific claims refer to the manuscript and associated reproducibility reports, including differences in training budget, reuse of validation data, single-farm data and retrospective use of test data.
