# Notebook inventory and recommended ordering

**Public source copies** were reconstructed from the 34 source notebooks in the study's Google Drive project on 20 October 2026. They have the same input cells, explanations and order, but output cells and prior runtime traces were cleared. The original executed notebooks were not modified. These source copies can still contain **legacy author-specific Drive paths**, which must be adapted on another account.

The original-numbered notebooks **00–33** are all accounted for. **25** is represented by the `CORREGIDO` canonical notebook and **26** by its explicitly marked `REVISION` version.

## Primary publication path

1. **00 → 01 → 02**: dataset retrieval, integrity review, fixed date partition.
2. **03, 06, 22**: YOLO11, Mask R-CNN and YOLO26 training recipes.
3. **31, 32**: additional seeds for YOLO11 and Mask R-CNN.
4. **09, 23, 33**: original COCO harmonization, YOLO26 COCO seeds, and final **nine-run COCO** evaluation.

Notebooks 04–08, 10–21 and 24–30 document the supporting geometry, count, calibration, uncertainty and qualitative interpretability analyses. They should **not** all be rerun before a reader can understand Experiment 33.

## Full canonical inventory

| Notebook | Scope | Drive source |
|---|---|---|
| [00_CERDOS_Descarga_CPU.ipynb](../notebooks/01_data/00_CERDOS_Descarga_CPU.ipynb) | `01_data` | [Original notebook](https://drive.google.com/file/d/1KE1k2zTltyHBfKVM2Z8QymqWWfKsK5bF/view) |
| [01_CERDOS_Auditoria_CPU.ipynb](../notebooks/01_data/01_CERDOS_Auditoria_CPU.ipynb) | `01_data` | [Original notebook](https://drive.google.com/file/d/1yiywzHpzRlzecjBMB_eQSS6LlcdQQLxp/view) |
| [02_CERDOS_Preparacion_Segmentacion_CPU.ipynb](../notebooks/01_data/02_CERDOS_Preparacion_Segmentacion_CPU.ipynb) | `01_data` | [Original notebook](https://drive.google.com/file/d/1x9jJEqxz06GkC40dx8V11H4rFTZoF1hB/view) |
| [03_CERDOS_Entrenamiento_YOLO11n_GPU.ipynb](../notebooks/02_training/03_CERDOS_Entrenamiento_YOLO11n_GPU.ipynb) | `02_training` | [Original notebook](https://drive.google.com/file/d/1Zk91zu6WgrGpLs1tYIv1hoFAKIc4op2m/view) |
| [04_CERDOS_Segmentacion_Evaluacion_GPU.ipynb](../notebooks/03_evaluation/04_CERDOS_Segmentacion_Evaluacion_GPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/1rioiOxG4y4asczxYt-6ppp9-9FvfGu7d/view) |
| [05_CERDOS_Auditoria_Resultados_CPU.ipynb](../notebooks/03_evaluation/05_CERDOS_Auditoria_Resultados_CPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/1I4HdqaolUpIcVR8aOSetRlcteak8_T_E/view) |
| [06_CERDOS_Entrenamiento_MaskRCNN_GPU.ipynb](../notebooks/02_training/06_CERDOS_Entrenamiento_MaskRCNN_GPU.ipynb) | `02_training` | [Original notebook](https://drive.google.com/file/d/1jzz49yUMaLP1BNgP_HUzkVt-V6wDYQ1k/view) |
| [07_CERDOS_Evaluacion_MaskRCNN_GPU.ipynb](../notebooks/03_evaluation/07_CERDOS_Evaluacion_MaskRCNN_GPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/195y9IB1nDfAHJ_2vvCX5TH0oqBjt_tok/view) |
| [08_CERDOS_Comparacion_Arquitecturas_CPU.ipynb](../notebooks/03_evaluation/08_CERDOS_Comparacion_Arquitecturas_CPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/1CyJlMehi-a-BkSO48_x6_ZVIxbG_SJUR/view) |
| [09_CERDOS_Evaluacion_Armonizada_COCO_GPU.ipynb](../notebooks/03_evaluation/09_CERDOS_Evaluacion_Armonizada_COCO_GPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/12xCKfHfx5Y1acaqsu2XT_ti1_G5ZICj2/view) |
| [10_CERDOS_Analisis_Fecha_Incertidumbre_CPU.ipynb](../notebooks/03_evaluation/10_CERDOS_Analisis_Fecha_Incertidumbre_CPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/1_FpzOJkpPA-8VK93He0CEQsNvP37pnWR/view) |
| [11_CERDOS_Confiabilidad_Geometrica_CPU.ipynb](../notebooks/03_evaluation/11_CERDOS_Confiabilidad_Geometrica_CPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/1XcgQIGFXj2jPXRdyO50u5QbqAydOUUv2/view) |
| [12_CERDOS_Eficiencia_Computacional_GPU.ipynb](../notebooks/03_evaluation/12_CERDOS_Eficiencia_Computacional_GPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/1QavEMk4yXSlTaLYqrBpuhqyMqtX9NPyB/view) |
| [13_CERDOS_Predicciones_Calibracion_Validacion_GPU.ipynb](../notebooks/04_calibration/13_CERDOS_Predicciones_Calibracion_Validacion_GPU.ipynb) | `04_calibration` | [Original notebook](https://drive.google.com/file/d/1XvzNXIif8M-WlZNh0JNSq_Gv3go82bbO/view) |
| [14_CERDOS_Calibracion_Probabilistica_CPU.ipynb](../notebooks/04_calibration/14_CERDOS_Calibracion_Probabilistica_CPU.ipynb) | `04_calibration` | [Original notebook](https://drive.google.com/file/d/14NodSwRyERY4F9d55DEEF1sVzvV2evvq/view) |
| [15_CERDOS_Correccion_Conteo_Umbrales_CPU.ipynb](../notebooks/04_calibration/15_CERDOS_Correccion_Conteo_Umbrales_CPU.ipynb) | `04_calibration` | [Original notebook](https://drive.google.com/file/d/1RKHrXJDBbDcdzlqqzL8Zl1I5m5Ey9K6_/view) |
| [16_CERDOS_Calibracion_Sensibilidad_ECE_CPU.ipynb](../notebooks/04_calibration/16_CERDOS_Calibracion_Sensibilidad_ECE_CPU.ipynb) | `04_calibration` | [Original notebook](https://drive.google.com/file/d/17FMSlBiujofr6L7Yw7uj7lYzpA_OVz7X/view) |
| [17_CERDOS_Auditoria_Fuentes_Sesiones_CPU.ipynb](../notebooks/03_evaluation/17_CERDOS_Auditoria_Fuentes_Sesiones_CPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/1L92TpW9orjplQs0wqgKZAzoRL2SKhPpP/view) |
| [18_CERDOS_Metrica_Tamano_Bootstrap_Sesion_CPU.ipynb](../notebooks/03_evaluation/18_CERDOS_Metrica_Tamano_Bootstrap_Sesion_CPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/1yx2ZL62eYE7dIVQ8K25dXiqKB8GBIEne/view) |
| [19_CERDOS_Mapas_Calor_Multidimensionales_CPU.ipynb](../notebooks/03_evaluation/19_CERDOS_Mapas_Calor_Multidimensionales_CPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/1YAxdefwPF8hONAseNDqqQhyKTl9uZC1J/view) |
| [20_CERDOS_GradCAM_Misma_Instancia_GPU.ipynb](../notebooks/06_explainability/20_CERDOS_GradCAM_Misma_Instancia_GPU.ipynb) | `06_explainability` | [Original notebook](https://drive.google.com/file/d/1KqeLmOTbDiiHeb0jzBQHdifRRbOFcDzM/view) |
| [21_CERDOS_Inferencia_Estadistica_Calibracion_CPU.ipynb](../notebooks/04_calibration/21_CERDOS_Inferencia_Estadistica_Calibracion_CPU.ipynb) | `04_calibration` | [Original notebook](https://drive.google.com/file/d/1ecxYeGQZdSpz_kmp3LKJhN1jyMRBLZKQ/view) |
| [22_CERDOS_Entrenamiento_YOLO26n_Semillas_GPU.ipynb](../notebooks/02_training/22_CERDOS_Entrenamiento_YOLO26n_Semillas_GPU.ipynb) | `02_training` | [Original notebook](https://drive.google.com/file/d/1C-g8xGEvPqVV0NQRbq3831BJN5C7Y3Qc/view) |
| [23_CERDOS_Evaluacion_YOLO26_COCO_3_Semillas_GPU.ipynb](../notebooks/03_evaluation/23_CERDOS_Evaluacion_YOLO26_COCO_3_Semillas_GPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/1Acff9xrTBoj2aaSayNaIOt8dsxiF4bS9/view) |
| [24_CERDOS_Auditoria_Errores_YOLO26_CPU.ipynb](../notebooks/05_diagnostics/24_CERDOS_Auditoria_Errores_YOLO26_CPU.ipynb) | `05_diagnostics` | [Original notebook](https://drive.google.com/file/d/19p5wW2dmsqhG-PD5Dd5vZjDCXR6yYbwY/view) |
| [CERDOS_25_Count_Diagnostics_CPU_CORREGIDO.ipynb](../notebooks/05_diagnostics/CERDOS_25_Count_Diagnostics_CPU_CORREGIDO.ipynb) | `05_diagnostics` | [Original notebook](https://drive.google.com/file/d/1kYKIiSy4QDsIuawcaufR372Vd7fk413K/view) |
| [26_CERDOS_Calibracion_Conteo_Validacion_GPU_REVISION.ipynb](../notebooks/05_diagnostics/26_CERDOS_Calibracion_Conteo_Validacion_GPU_REVISION.ipynb) | `05_diagnostics` | [Original notebook](https://drive.google.com/file/d/1FFPmoFV9E86G5cxdRXE57Vc-CW81ICIX/view) |
| [27_CERDOS_Evaluacion_Conteo_Calibrado_CPU.ipynb](../notebooks/05_diagnostics/27_CERDOS_Evaluacion_Conteo_Calibrado_CPU.ipynb) | `05_diagnostics` | [Original notebook](https://drive.google.com/file/d/1nDzNqYHaAIG8F_sSwXQudDBu3dINdDyX/view) |
| [28_CERDOS_Robustez_Estadistica_Conteo_CPU.ipynb](../notebooks/05_diagnostics/28_CERDOS_Robustez_Estadistica_Conteo_CPU.ipynb) | `05_diagnostics` | [Original notebook](https://drive.google.com/file/d/1IGkdfpezf1d0Ldkn8xAJNzdcDsEGitzh/view) |
| [29_CERDOS_Analisis_Casos_Criticos_CPU.ipynb](../notebooks/05_diagnostics/29_CERDOS_Analisis_Casos_Criticos_CPU.ipynb) | `05_diagnostics` | [Original notebook](https://drive.google.com/file/d/1VfX6tnxKfgjdJABJe0hMLKYKW4I-F2x3/view) |
| [30_CERDOS_Analisis_Visual_Errores_CPU.ipynb](../notebooks/05_diagnostics/30_CERDOS_Analisis_Visual_Errores_CPU.ipynb) | `05_diagnostics` | [Original notebook](https://drive.google.com/file/d/1W0OZqKTYEUu8qbJGsXaB2LtmIX6B7ztK/view) |
| [31_CERDOS_Repeticiones_YOLO11n_GPU.ipynb](../notebooks/02_training/31_CERDOS_Repeticiones_YOLO11n_GPU.ipynb) | `02_training` | [Original notebook](https://drive.google.com/file/d/1EaAV0QZntERhxj6AL5_E5QTtvHuYY0TI/view) |
| [32_CERDOS_Repeticiones_MaskRCNN_GPU.ipynb](../notebooks/02_training/32_CERDOS_Repeticiones_MaskRCNN_GPU.ipynb) | `02_training` | [Original notebook](https://drive.google.com/file/d/19bKRb0C_mwwoWe1qNX_Peo9VXmE_fVK9/view) |
| [33_CERDOS_Evaluacion_COCO_9_Semillas_GPU.ipynb](../notebooks/03_evaluation/33_CERDOS_Evaluacion_COCO_9_Semillas_GPU.ipynb) | `03_evaluation` | [Original notebook](https://drive.google.com/file/d/1nsEHU57LTLLV3QmkIri31-WDo9AkE0j0/view) |

Source file IDs and both raw and cleaned-file SHA-256 digests are in [`NOTEBOOK_PROVENANCE.json`](NOTEBOOK_PROVENANCE.json).
