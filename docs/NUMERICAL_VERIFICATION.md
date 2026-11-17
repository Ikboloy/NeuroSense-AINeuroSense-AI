# Numerical verification — 2026-11-17

## Inputs and scope

Independent recalculation used the user's original archive `NeuroSense_AI.zip`, extracting:
- `dataset/scene1/disp0GT.pfm` (2000 × 2964)
- `results_272/sgbm_disparity.npy` (2000 × 2964)
- `dataset/scene1/calib.txt` (fx = 3979.911 px, baseline = 0.193001 m, doffs = 124.343 px)
- `results_17/motorcycle_mask_refined.png`

The numerical definitions were compared against original `experiment19b.py` and `experiment20.py`, and computed output compared with original CSVs. This verifies **metrics from existing prediction/reference arrays**, not end-to-end regeneration of the prediction from source images, nor external validation of the dataset.

## Experiment 19B — verified

| Region | GT valid | Common valid | Coverage (%) | Disparity MAE (px) | Depth MAE (m) |
|---|---:|---:|---:|---:|---:|
| Full scene | 5761176 | 4713161 | 81.81 | 2.5439 | 0.0338 |
| Motorcycle mask | 1846886 | 1678811 | 90.90 | 3.5766 | 0.0385 |
| Outside mask | 3914290 | 3034350 | 77.52 | 1.9726 | 0.0313 |

All rows match the archived `results_19/ground_truth_depth_metrics.csv` to its published rounding precision.

## Experiment 20 — verified

| Depth range | GT valid | Common valid | Coverage (%) | Depth MAE (m) | Depth p95 (m) | Disparity MAE (px) |
|---|---:|---:|---:|---:|---:|---:|
| 0–1m | 0 | 0 | NA | NA | NA | NA |
| 1–2m | 0 | 0 | NA | NA | NA | NA |
| 2–3m | 3068898 | 2752915 | 89.70 | 0.0113 | 0.0187 | 1.2546 |
| 3–5m | 2691795 | 1960246 | 72.82 | 0.0655 | 0.3175 | 4.3546 |
| 5–20m | 483 | 0 | 0.00 | NA | NA | NA |

All rows match archived `results_20/distance_depth_metrics.csv` to its published rounding precision.

## Chess1 status — NOT independently rerun

Archived `results_14/confidence_metrics.csv` and `results_16/near_surface_metrics.csv` were inspected, but stereo matching was **not rerun** to regenerate their values. Experiment 16's `CONFIDENCE_AWARE` and `STRICT_LR` output rows are numerically identical, so no separate evaluated caution/unknown alert policy can be claimed.

## Remaining JOSS work

- Re-run original StereoSGBM image-to-disparity pipeline from inputs.
- Run packaged `neurosense_ai.cli` directly on the original data and compare outputs.
- Integrate Chess1 experiments 14 and 16 and verify against their CSVs.
- Add data acquisition/permissions, regression fixtures, full documentation, and sustained development evidence.
- No navigation safety, haptic performance or human-subject outcomes have been evaluated.
