# Runtime and package provenance

## Recorded evaluation environment (experiment 33)

- GPU: NVIDIA L4 (experiment 33)
- Python: **3.13.15**
- PyTorch: **2.11.0+cu130**
- torchvision: **0.26.0+cu130**
- Ultralytics: **8.4.182**
- COCO evaluation: `pycocotools`, instance mask (`iouType=segm`), IoUs 0.50–0.95 in 0.05 steps, `maxDets=[1,10,100]`.

The original 2026 YOLO11/Mask R-CNN training ran on **Tesla T4**; later runs include **L4**. The historical run notebooks may install dependencies differently, including preinstalled CUDA-specific PyTorch builds. **Do not blindly replace CUDA-enabled torch with a CPU wheel.** Read notebook package-installation cells before execution.

The supplied `requirements-analysis.txt` is a **minimum installation aid**, not a resolved exact dependency lock. For byte-for-byte execution-environment reproduction, a container image or complete Colab snapshot has not yet been published. Reproducibility claims are scoped accordingly.

## Core methodological settings

| Item | YOLO11n-seg | YOLO26n-seg | Mask R-CNN ResNet50-FPN |
|---|---|---|---|
| Seeds | 2026, 2027, 2028 | 2026, 2027, 2028 | 2026, 2027, 2028 |
| Epoch cap | 60 | 60 | 12 |
| Batch size | 8 | 8 | 1 |
| Image size | 640 | 640 | min 512, max 768 |
| Optimizer | Ultralytics `auto` | See notebook 22 run configs | AdamW, LR=1e-4, weight decay=1e-4 |
| Checkpoint choice | Best validation mask AP | Best validation mask AP | Best validation mask AP |

The budget is **not equalized** across model families; this study compares trained configurations, not architecture effects under identical compute budgets.
