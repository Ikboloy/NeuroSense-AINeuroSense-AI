# Chess1 — package-level reproduction

The `neurosense_ai.chess1` module refactors the original `experiment12.py`, `experiment14.py` and `experiment16.py` into reusable functions without importing the original scripts.

## Required inputs

Obtain the Chess1 scene from Middlebury (subject to its terms) and place these files in a single directory: `im0.png`, `im1.png`, `disp0.pfm`, `calib.txt`.

## Command

```bash
python -m pip install -e '.[experiments,test]'
python -m neurosense_ai.chess1_cli --scene dataset/middlebury/chess1 --output results/chess1
```

The outputs are `confidence_metrics.csv` and `near_surface_metrics.csv`.

## Expected archived results

- Experiment 14: VALID 1,024,634 pixels (57.97%, MAE 4.1764 px), UNCERTAIN 274,671 (15.54%, MAE 13.9023 px), INVALID 468,231 (26.49%).
- Experiment 16: BASELINE TP 922,679, FN 146,303, FP 44,658; STRICT_LR TP 746,849, FN 322,133, FP 29,609.

**Important:** CONFIDENCE_AWARE is intentionally identical to STRICT_LR in the original script; no separate caution policy was evaluated.

## Regression test (full dataset)

The repository includes `tests/test_chess1_regression.py`, which compares every reported confidence and near-surface CSV metric with the archived results.

Linux/macOS:

```bash
python -m pip install -e '.[test]'
NEUROSENSE_CHESS1_DIR=dataset/middlebury/chess1 python -m pytest -q tests/test_chess1_regression.py
```

Windows PowerShell:

```powershell
python -m pip install -e '.[test]'
$env:NEUROSENSE_CHESS1_DIR = "dataset/middlebury/chess1"
python -m pytest -q tests/test_chess1_regression.py
```

Without `NEUROSENSE_CHESS1_DIR`, this full-data test is intentionally **skipped**, not passed. The CI's regular unit tests do not verify the numerical results without the Middlebury images.

## Verification status

The original experiments were previously re-executed against the original Chess1 images, but this **newly refactored package implementation has not yet been run on the full Chess1 dataset**. Synthetic unit tests alone do not demonstrate numerical reproduction. Do not report this package as independently validated until the generated CSVs are compared field-by-field to the archived originals.

Dependencies and OpenCV implementation differences may affect pixel-level outputs.


## Independent numerical verification — 2026-11-17

The full Chess1 images and reference PFM in the author's original `NeuroSense_AI.zip` archive were processed in a clean, standalone Python calculation using the same StereoSGBM and LR-consistency operations as the package implementation. OpenCV version: **4.13.0**. Calibration: `fx=1758.23` pixels, `baseline=111.53` mm, `doffs=0`, `ndisp=290`; original image size: 1920 × 1080; processing scale: 0.5.

**Result:** every value in all three Experiment 14 confidence rows and all three Experiment 16 near-surface rows matched the archived CSV files exactly (including rounding and `nan` cells). The matching counts and percentages are shown above and in `docs/CHESS1_REEXECUTION.md`.

**Scope clarification:** this independent calculation follows the package implementation but did not import the installed package directly. The new opt-in regression test is provided to verify the actual installed package on machines with the Chess1 dataset. GitHub Actions cannot perform that full-data check because the dataset is not included. The ordinary unit-test CI passed on the latest commit before this documentation update.

The original experiment and the package intentionally give identical `STRICT_LR` and `CONFIDENCE_AWARE` metrics. This does not demonstrate a distinct confidence-aware policy.
