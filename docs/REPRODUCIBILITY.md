# Reproducing the experimental pipeline

## Independent numerical audit — completed

[Independent COCO audit](INDEPENDENT_COCO_AUDIT.md): a separately implemented RLE mask evaluator reproduced **9 global and 45 date-level sets of AP, AP50 and AP75**, a total of **162 scalar comparisons** with maximum deviation 3.33e-16 from Experiment 33. Nine input prediction hashes and the GT file hash were checked against frozen provenance. This is not new inference/training and not an official `pycocotools` rerun; raw mask files are not redistributed here.

## Verification levels

1. **Static repository verification**: `python scripts/audit_repository.py` checks the frozen manifests, notebooks, JSON results and nine-by-five date structure. This does **not** rerun inference.
2. **Historical-record verification**: the archived prediction JSON and GT SHA-256 inputs were rechecked in the independent audit; complete checkpoint verification and a fresh environment rerun remain separate.
3. **Full computational rerun**: obtain FaroPigSeg from its authors, reconstruct the frozen date split, train and select nine models, generate COCO predictions with exactly recorded model settings, and rerun COCOeval. Requires GPU time and matching software.

**Full level 2 / level 3 verification requires artifacts that are not wholly hosted in this repository** (data, weights, complete original prediction JSONs) and should never be advertised as satisfied by a green CI badge.

## Preparation

- Clone this repository.
- Fetch FaroPigSeg from the official upstream project and respect CC BY-NC 4.0.
- Verify `data/partitions/particion_fecha_manifest.json` and SHA-256. Split is **by acquisition date**, not by the upstream physical folder labels.
- Use `python scripts/rebase_split_lists.py --dataset-root <extracted_FaroPigSeg> --out-dir outputs/local_split --strict` and keep resulting local split files **outside Git**.
- Mount Google Drive in Colab; adapt the legacy hardcoded project roots in notebook cells, including input YAML and `03_Resultados` output directories.

## Primary experiment order

| Stage | Canonical notebooks | Reproduction purpose |
|---|---|---|
| Data preparation | 00, 01, 02 | Download, audit and create frozen date split |
| Initial training | 03, 06, 22 | Original YOLO11, Mask R-CNN, YOLO26 seeds |
| Additional seeds | 31, 32 | YOLO11 and Mask R-CNN seeds 2027/2028; preserve 2026 |
| Base evaluation | 09 and 23 | COCO original models and YOLO26 three seeds |
| Main final evaluation | **33** | Harmonized COCO 9-seed comparison on 373 test images |

Notebook 33 is an **integrator**, not a standalone one-click solution: it expects the historical prediction files and trained checkpoint artifacts produced by earlier stages. Do not claim nine-seed reproduction by running only notebook 33.

## Extended analyses (secondary)

- 04, 05, 07, 08, 10, 11, 12, 17–19: segmentation, geometry, date effects, computational diagnostics.
- 13–16, 21: original 2026 model confidence-calibration analyses and threshold diagnostics.
- 24–30: YOLO26 count-error exploratory follow-up, operational calibration, difficult cases. **25 is the corrected canonical version** and **26 the revision**; no obsolete drafts are shipped.
- 20: same-pig Grad-CAM visualizations, **qualitative** because YOLO and Mask R-CNN attribution domains differ.

These later investigations reused validation/test data. They are reported retrospectively; the date split does not retroactively make the test prospectively untouched.

## Main COCO controls

`iouType=segm`; IoU thresholds 0.50:0.05:0.95; `maxDets=[1,10,100]`. YOLO11: `imgsz=640, conf=0.001, iou=0.7, max_det=100, retina_masks=True`; Mask R-CNN: `min_size=512, max_size=768, score_thresh=0.001, detections_per_img=100, mask threshold=0.5`. YOLO26 predictions originate in notebook 23 with their own recorded original protocol; consult it before re-evaluating. Results reflect 373 test images and 4,648 mask annotations across five acquisition dates.

## Known inference/claim boundaries

- Training starts from differing pretrained weights, schedules, image resizing and optimizers.
- Only **five dates** are test groups; do not use the three seeds as if they added independent acquisition dates.
- Score calibration/Platt and the historical counting analysis are not all-nine-model assessments.
- Time benchmarking is device/precision-specific and not a Jetson/edge deployment claim.
- No independently acquired external farm is evaluated in this manuscript.

See [NOTEBOOK_INDEX.md](NOTEBOOK_INDEX.md), [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) and [../results/README.md](../results/README.md).
