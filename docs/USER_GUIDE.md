# NeuroSense AI — user guide

## What the software does

NeuroSense AI is a research prototype for **offline** rectified stereo depth and confidence/error evaluation. It provides:
1. Chess1 StereoSGBM image-to-disparity, signed LR consistency, confidence partition and near-surface metrics.
2. Motorcycle/reference disparity-to-depth scene metrics and distance-bin summaries.
3. Metric RGB point-cloud reconstruction and PLY export.

It is **not** a real-time assistive device, haptic navigation system, or validated safety-critical application.

## Requirements

Python >= 3.10; NumPy; OpenCV for image experiments; pytest for testing.

```bash
python -m pip install -e '.[experiments,test]'
python -m pytest -q
```

## Chess1

Obtain `im0.png`, `im1.png`, `disp0.pfm` and `calib.txt` from Middlebury. No dataset is bundled.

```bash
python -m neurosense_ai.chess1_cli --scene /path/to/chess1 --output results/chess1
```

Run the **opt-in full-data regression** with `NEUROSENSE_CHESS1_DIR` set to the scene directory. Otherwise pytest reports the regression as **skipped**.

## Motorcycle depth metrics

Obtain `disp0GT.pfm`, `calib.txt` and a generated `sgbm_disparity.npy`:

```bash
python -m neurosense_ai.cli --prediction sgbm_disparity.npy --reference disp0GT.pfm --calibration calib.txt --mode scene --output results/motorcycle_scene.csv
python -m neurosense_ai.cli --prediction sgbm_disparity.npy --reference disp0GT.pfm --calibration calib.txt --mode bins --output results/motorcycle_bins.csv
```

## 3D reconstruction

See `docs/POINTCLOUD_REPRODUCTION.md` for the Python API and `docs/MOTORCYCLE_3D_VERIFICATION.md` for numerical verification against the original PLY.

## Metric interpretation

Coverage is the fraction of ground-truth-valid pixels where the prediction is valid. Rejected/unknown pixels are **not safe free space**. A lower error on accepted pixels can coincide with reduced coverage and recall. A confidence partition is an offline diagnostic, not a calibrated probability of safety.

## Reproducibility and ethics

- Original experiment scripts and the refactored library have different packaging; archived CSV matching does not imply independent validation on a new dataset.
- OpenCV implementation/platform differences can alter stereo disparities.
- Middlebury licensing applies to the input images; the MIT license applies only to this project's original source code.
- No tests involving blind/low-vision participants or haptic-device outcomes have been conducted.
