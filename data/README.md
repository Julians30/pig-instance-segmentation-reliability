# FaroPigSeg: data acquisition and frozen split

Do **not** add the upstream images, YOLO labels, dataset ZIP, or derived ground-truth masks to this repository. This dataset is supplied by its authors under **CC BY-NC 4.0** and must be obtained separately: https://github.com/yudong888/FaroPig-Datasets/tree/main/FaroPigSeg.

The `partitions/` files here are the **exact original files used by the recorded experiments**. They retain absolute paths under the original Colab `/content/drive/MyDrive/...` root so their published SHA-256 fingerprints can be audited. They are not portable without adaptation. The upstream dataset's physical `train/val/test` folders are not our date split; image paths must be selected by **the frozen manifest**.

### Build a local split

```bash
python scripts/rebase_split_lists.py \
  --dataset-root /path/to/extracted/FaroPigSeg \
  --out-dir outputs/local_split --strict
```

The resulting `data_fecha_local.yaml` and the `train.txt`, `val.txt`, `test.txt` lists are new **machine-specific** derivatives; do not mistake their hashes for the original published SHA-256 values.

### Original file fingerprints (SHA-256)

- `particion_fecha_manifest.json`: `27ba2e77c188d360bc5d6cbac2a2e2bf0ec929448ae082e49e583e222ad48cd3`
- `data_fecha_original.yaml`: `9a223b47038c661303c1d12a35cbdcb212ed51529c8c773c4c9c66998706d1d9`
- `train.txt`: `17b343f693a62714ebe0d1629b30ec8daff9c7081a1f4234f90ab11107921281`
- `val.txt`: `6368e3c82d001e33035cdb46ea6c7882ad599d22a06d885a22d8177549619e9d`
- `test.txt`: `0d31f2b3bc931c6f08c96544df8fdb1f91c3b6bea5da4624917e94da97e01c05`

If the original archive was modified upstream or its directory layout changes, re-examine the mapping rather than silently modifying the frozen split.
