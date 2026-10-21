# Pig instance segmentation reliability: a multidimensional assessment

[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](LICENSE)
[![Dataset: CC BY-NC 4.0](https://img.shields.io/badge/Upstream%20Data-CC%20BY--NC%204.0-lightgrey.svg)](DATA_LICENSE.md)
[![Repository integrity](https://github.com/Julians30/pig-instance-segmentation-reliability/actions/workflows/repository-audit.yml/badge.svg)](.github/workflows/repository-audit.yml)

**Research code and documented experimental artifacts** for the manuscript *Multidimensional Reliability of Pig Instance Segmentation: Three Architectures Across Three Training Seeds* (planned submission to *Smart Agricultural Technology*, Elsevier). The manuscript is **not yet published or accepted**.

**Researchers:** Julián Coronel-Reyes and Alexander Haro-Sarango. The repository includes **34 clean Colab notebooks** (numbered 00–33; notebook 25 is the corrected version), frozen date-disjoint split manifests, records of the nine-seed COCO assessment, manuscript-oriented figures and automated integrity checks.

## Research question and experimental scope

What do three pig instance-segmentation **training configurations** reveal about accuracy and reliability beyond a single mask AP score? We compare **YOLO11n-seg**, **YOLO26n-seg**, and **Mask R-CNN ResNet50-FPN**, each trained with seeds **2026, 2027 and 2028**. We examine date-wise segmentation performance, geometry, counting thresholds, probabilistic calibration, efficiency and exploratory Grad-CAM maps.

**Key design limitations:** training budgets differ by architecture (YOLO up to 60 epochs, batch 8; Mask R-CNN 12 epochs, batch 1). The date-disjoint test is from the **same dataset/farm**, was consulted in earlier analyses, and **is not external-farm validation**. Differences are descriptive; three seeds are not nine independent test sessions. Calibration and the counting operating-point analyses originated from the 2026 configurations and are not asserted to cover all nine runs.

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

The code publication contains notebook source cells with executed outputs stripped, split files copied byte-for-byte, original small experiment reports, nine-seed summaries and self-checks for counts/date separation/checksums. It does **not** ship model weights, the FaroPigSeg images, ground-truth masks, or a fully containerized end-to-end GPU reproduction. The original Colab notebooks also include environment-specific paths; details and remaining items are maintained in [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md).

## Code/data availability, citation and licenses

- Project code/documentation: **MIT**, [`LICENSE`](LICENSE). The MIT license does **not** supersede third-party data or model licenses.
- Original FaroPigSeg data: **CC BY-NC 4.0**. See [`DATA_LICENSE.md`](DATA_LICENSE.md).
- Please cite the upstream FaroPigSeg article: *Housed Pig Identification and Tracking for Precision Livestock Farming*, *Expert Systems with Applications*, 293 (2025), 128466, https://doi.org/10.1016/j.eswa.2025.128466.
- Software citation metadata: [`CITATION.cff`](CITATION.cff); no DOI or publication status is invented for the present study.

For scientific claims refer to the manuscript and associated reproducibility reports, including differences in training budget, reuse of validation data, single-farm data and retrospective use of test data.
