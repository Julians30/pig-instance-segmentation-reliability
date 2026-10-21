# Data provenance, licenses and redistribution

**The MIT license in this repository covers original project code and documentation, not external datasets or pretrained network weights.**

- **Upstream data:** FaroPigSeg, from the official FaroPig-Datasets project: https://github.com/yudong888/FaroPig-Datasets/tree/main/FaroPigSeg
- **Dataset license:** Creative Commons Attribution–NonCommercial 4.0 International (**CC BY-NC 4.0**), as indicated by the upstream repository. The user must review the authoritative upstream terms.
- **Dataset publication:** *Housed Pig Identification and Tracking for Precision Livestock Farming*, *Expert Systems with Applications* **293**, article 128466 (2025); https://doi.org/10.1016/j.eswa.2025.128466
- **Not distributed here:** the source photographs, ground-truth segmentation polygons, dataset archive, dataset-derived COCO ground truth, and third-party pretrained checkpoints.
- **Distributed here:** author-produced code, evaluation summaries, split filename lists and source provenance metadata. See `results/README.md` for the precise status of model predictions.

The original training, validation and test filename manifests identify filenames and acquisition dates but **not the underlying image data**. They are provided to reproduce the published experimental split. Respect the dataset's conditions when downloading and using it. Do not assume that MIT relicenses the underlying images, annotations or derivative works.
