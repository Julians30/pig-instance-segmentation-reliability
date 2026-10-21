# Scientific and reproducibility limitations

1. **Single farm/source dataset.** Date-disjoint splitting prevents date overlap but does not test domain shift between farms, cameras or management settings. External-farm validation is a separate future study.
2. **Unequal training budgets.** YOLO: 60 epochs/batch 8; Mask R-CNN: 12 epochs/batch 1. Validation curves and three seeds support descriptive comparison but cannot identify a pure architectural effect.
3. **Small number of dates.** Only five test acquisition dates. The smallest exact two-sided sign-test p value with five nonzero paired date differences is 0.0625. Treat per-date contrasts descriptively; confidence statements about unseen dates/farms are limited.
4. **Validation reuse.** The same 196 images were used for checkpoint choice and later calibration/counting thresholds. Threshold/calibration results can be optimistic.
5. **Retrospectively inspected test.** Test images were consulted in successive exploratory notebooks before the nine-seed summary. Do not label them a prospectively untouched test.
6. **Calibration scope.** Original Platt and ECE comparisons for YOLO11 and Mask R-CNN 2026 are not estimates for all nine seeds or YOLO26.
7. **Grad-CAM scope.** The full-frame attribution for YOLO and ROI-based attribution for Mask R-CNN should not be compared as quantitative measures of interpretability.
8. **Runtime portability.** Colab notebooks refer to a named Drive project root and can depend on installed CUDA packages. Clean notebook sources do not alone guarantee automated rerun.
9. **Weights and third-party data absent.** The repository omits FaroPigSeg images, labels and model checkpoints. Logs, manifests and small results are supplied; heavy artifacts require separate access/permission review.
10. **Numerical records vs recomputation.** A passing GitHub Actions workflow checks dataset split integrity and recorded results; it does not prove the historical AP values have been independently recalculated from all predicted masks.
