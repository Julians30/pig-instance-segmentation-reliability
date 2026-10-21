# Reviewer quick-start and evidence map

> **Status:** source-code and artifact documentation release. Automated GitHub Actions tests perform **static provenance and consistency checks**, not GPU training or independent COCO mask AP recalculation. The manuscript is a planned submission to *Smart Agricultural Technology*, not an accepted publication.

## Read this first

1. [Main README](../README.md): scope, headline COCO results and boundaries.
2. [Notebook index](NOTEBOOK_INDEX.md): **34 sequential notebooks** (00–33, with the corrected canonical notebook 25) grouped by function.
3. [Reproduction instructions](REPRODUCIBILITY.md): data setup, original Drive-path handling and run sequence.
4. [Environment provenance](../environment/README.md): versions and unequal compute budgets.
5. [Limitations](KNOWN_LIMITATIONS.md): single source farm, five independent test dates, validation reuse and retrospective analyses.
6. [Data license](../DATA_LICENSE.md): obtain FaroPigSeg separately; **CC BY-NC 4.0** is not superseded by the MIT *code* license.

## Newly completed independent numerical verification

A standalone Python/NumPy implementation has recomputed COCO mask AP from nine saved RLE prediction files and the same GT. **All 162 global and date-level AP/AP50/AP75 metrics agree**, maximum absolute discrepancy 3.33e-16. Consult [the independent COCO audit](INDEPENDENT_COCO_AUDIT.md) and its [machine-readable report](../results/reports/INDEPENDENT_COCO_AUDIT_RESULT.json). This establishes **numeric repeatability from archived predictions**, not a fresh network-training replication or generalization to new farms.

## Manuscript-to-artifact map

| Scientific statement | Primary notebooks | Public artifact | Verification status |
|---|---|---|---|
| Frozen date-disjoint split (949/196/373 images; 16/4/5 dates) | 00–02 | `data/partitions/`, `scripts/rebase_split_lists.py` | Manifest/count/hash tested by CI; original data not redistributed |
| Nine trained configurations (3 architectures × 3 seeds) | 03, 06, 22, 31, 32 | `results/reports/CERDOS_31_Training_Report.json`, `CERDOS_32_Training_Report.json`, `docs/NOTEBOOK_PROVENANCE.json` | Training records published; checkpoints not hosted |
| Harmonized COCO mask AP on 373 test images / 4,648 ground-truth instances | 09, 23, **33** | `results/reports/CERDOS_33_Informe_Final.json`, `CERDOS_33_Protocolo.json`, `results/tables/CERDOS_33_COCO_9_Semillas.xlsx` | 9-run results independently recalculated by separate NumPy COCO-style RLE evaluator; raw predictions/GT not all hosted; official pycocotools rerun not completed |
| Descriptive differences by acquisition date (5 dates) | 10, 17, 18, 23, **33** | `results/tables/CERDOS_33_per_date_metrics.csv`, `results/figures/CERDOS_33_AP_By_Date.png` | Date-level records audited; five dates cannot support strong unseen-farm inference |
| Training and validation trajectories | 03, 06, 22, 31, 32 | Validation records in training reports; original full logs in Drive | Different epochs, batch sizes and runtimes; not a compute-matched architecture study |
| Geometry, runtime and model outputs | 11, 12, 19 | Relevant notebook code | Architecture- and device-specific, not an edge-deployment validation |
| Confidence calibration (2026 configurations) | 13, 14, 16, 21 | Notebook code and corresponding historical Drive reports | Original-model-only; not nine-seed calibration |
| Counting thresholds and detection errors | 15, 24–30 | Notebook code | Validation tuning, retrospective test diagnostics, not prospective threshold confirmation |
| Same-instance Grad-CAM | 20 | Notebook source | Exploratory and qualitative; YOLO full-frame and Mask R-CNN ROI attributions are not directly comparable |

## Minimal checks without GPU

```bash
git clone https://github.com/Julians30/pig-instance-segmentation-reliability.git
cd pig-instance-segmentation-reliability
python scripts/audit_repository.py
```

The expected **PASS** verifies the manifest/date partition, SHA-256 fingerprints, 34 clean notebooks and 9 global/45 date-level reported COCO entries. It does **not** verify that the archived scores are correct by recomputing mask overlaps.

## Full computational reproduction is a separate level

The complete historical workflow requires the original FaroPigSeg images/labels under their upstream license, the recorded model checkpoints or a full GPU retraining run, reference COCO ground truth, all prediction JSONs, and environment-specific dependency installation. Some historical notebooks contain absolute Google Drive paths; see [REPRODUCIBILITY.md](REPRODUCIBILITY.md) before use. **Notebook 33 is an integrator and should not be represented as a standalone fresh nine-model rerun.**

The independent numerical audit from archived prediction masks is complete. Remaining improvements are checkpoint/prediction access instructions subject to license, independent official-`pycocotools` verification, portable notebook paths or execution wrappers, and a precise environment lock. Any claims about these levels should be updated *only after successful verification*.

## Ethics and external validity

No live-animal work or new-farm video is introduced here. The image dataset is a third-party public research resource. External-farm validation is intentionally reserved for a distinct follow-up research study; it is **not** performed or claimed in this repository.
