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

## Verification status

The original experiments were previously re-executed against the original Chess1 images, but this **newly refactored package implementation has not yet been run on the full Chess1 dataset**. Synthetic unit tests alone do not demonstrate numerical reproduction. Do not report this package as independently validated until the generated CSVs are compared field-by-field to the archived originals.

Dependencies and OpenCV implementation differences may affect pixel-level outputs.
