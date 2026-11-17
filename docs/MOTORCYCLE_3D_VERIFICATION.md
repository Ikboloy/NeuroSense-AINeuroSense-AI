# Motorcycle 3D point-cloud numerical verification

**Date:** 2026-11-17. **Source:** original user-provided `NeuroSense_AI.zip`.

## Inputs

- `dataset/scene1/im0.png`
- `dataset/scene1/calib.txt`
- `results_272/sgbm_disparity.npy`
- `results_272/neurosense_pointcloud.ply`
- Original `reconstruct3d.py`

## Independent results

The original `reconstruct3d.py` was executed against the archive's image, calibration and predicted disparity. It generated **301,197** points with a depth range of approximately **1.94–6.15 metres**. Its PLY and the archived PLY have **exactly identical text lines** (301,207 lines including the 10-line header). Byte-level hashes differ because the archived file uses different line endings; this is not a geometry discrepancy.

The refactored `disparity_to_points` geometry was independently recalculated with NumPy float64. It also generated **301,197** points. Compared with the archived PLY:
- **Maximum absolute XYZ difference:** 0.0000052 metres (approximately 5.2 micrometres), including PLY 5-decimal-place rounding.
- **RGB values:** exact equality for all 301,197 points.
- **Point ordering:** identical.

A local, opt-in package regression test was added at `tests/test_pointcloud_regression.py`. It is skipped by default because the third-party image and archived PLY are not redistributed. The comparison above is an independent recalculation using the package's equations; **the installed package regression test itself has not yet been executed against the dataset**.

## Run package regression

Create a directory containing `im0.png`, `calib.txt`, `sgbm_disparity.npy` and `archived_pointcloud.ply`, then:

```bash
python -m pip install -e '.[test]'
NEUROSENSE_MOTORCYCLE_DIR=/path/to/motorcycle python -m pytest -q tests/test_pointcloud_regression.py
```

PowerShell:

```powershell
$env:NEUROSENSE_MOTORCYCLE_DIR = "C:\\path\\to\\motorcycle"
python -m pytest -q tests/test_pointcloud_regression.py
```

These are **offline reconstruction metrics**, not a navigation or haptic-device safety evaluation.
