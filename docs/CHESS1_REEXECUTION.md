# Chess1 end-to-end re-execution — 17 November 2026

## Source and procedure

Original user-supplied `NeuroSense_AI.zip` was opened and the **unmodified original scripts** `experiment10.py`, `experiment12.py`, `experiment14.py`, and `experiment16.py` were executed against the original Chess1 Middlebury files:
- `dataset/middlebury/chess1/im0.png`
- `dataset/middlebury/chess1/im1.png`
- `dataset/middlebury/chess1/disp0.pfm`
- `dataset/middlebury/chess1/calib.txt`

The execution used Python with OpenCV **4.13.0**, at 50% image scale, StereoSGBM with 9-pixel block, and LR tolerance 1.0 pixel. Both scripts completed successfully. CSV contents were compared with the CSV files preserved in the original ZIP. **All field names, values and row ordering match**. Line-ending differences (CRLF in archive versus LF in the runtime text read) are not numerical differences.

This constitutes image-to-disparity-to-metric re-execution for Chess1. It is not yet a reproduction using the new installable `neurosense_ai` package.

## Experiment 14: confidence partition

| State | Ground-truth-valid pixels | Share (%) | Disparity MAE (px) | Bad2 (%) |
|---|---:|---:|---:|---:|
| VALID | 1,024,634 | 57.97 | 4.1764 | 24.35 |
| UNCERTAIN | 274,671 | 15.54 | 13.9023 | 36.05 |
| INVALID | 468,231 | 26.49 | NA | NA |

## Experiment 16: near-surface threshold 1.5 m

| Strategy | TP | FN | FP | Recall (%) | FNR (%) | Precision (%) | Unknown (%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| BASELINE | 922,679 | 146,303 | 44,658 | 86.31 | 13.69 | 95.38 | 26.49 |
| STRICT_LR | 746,849 | 322,133 | 29,609 | 69.87 | 30.13 | 96.19 | 42.03 |
| CONFIDENCE_AWARE | 746,849 | 322,133 | 29,609 | 69.87 | 30.13 | 96.19 | 42.03 |

The third strategy is **identical in the original code** to STRICT_LR; it is not evidence that a separate unknown/caution alert policy was evaluated.

## Remaining scope

- Motorcycle full-resolution StereoSGBM **image-to-disparity** regeneration has **not** yet been established, because the original image-to-disparity generation script and its exact parameters/provenance were not identified in this verification. Prior Motorcycle depth MAE checks use the already stored prediction array.
- Re-execute the same Chess1 pipeline from the new reusable library, without relying on the original experiment scripts.
- Confirm reproducibility across OpenCV versions and platforms.
- Document dataset acquisition, exact OpenCV dependencies and licensing.

The results do **not** establish pedestrian navigation safety or real-world haptic-device performance.
