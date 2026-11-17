# Offline depth evaluation: original experiments 19B and 20

This repository now includes a **reusable implementation of the metric definitions** from the uploaded original `experiment19b.py` and `experiment20.py` scripts.

The original Motorcycle scene used `dataset/scene1/disp0GT.pfm`, `dataset/scene1/calib.txt`, and `results_272/sgbm_disparity.npy`. These are **not distributed** here. Obtain Middlebury images/calibration/reference from the original source and generate a predicted disparity array independently.

## Run

```bash
python -m pip install -e '.[test]'
python -m neurosense_ai.cli --mode scene --prediction results_272/sgbm_disparity.npy --reference dataset/scene1/disp0GT.pfm --calibration dataset/scene1/calib.txt --output results/scene_metrics.csv
python -m neurosense_ai.cli --mode bins --prediction results_272/sgbm_disparity.npy --reference dataset/scene1/disp0GT.pfm --calibration dataset/scene1/calib.txt --output results/depth_bins.csv
```

The scene command computes full-scene coverage, disparity MAE and depth MAE. The bins command computes metrics for [0,1), [1,2), [2,3), [3,5), [5,20) metres. Original experiment19B also computed mask and outside-mask regions, which are **not yet exposed through this CLI**.

## Important limitations

This is a metric extraction and refactoring step, **not a reproduction of the published numeric results**. The Middlebury data and original prediction array have not been executed together in CI. The full StereoSGBM pipeline and other original experiments are not yet integrated. The evaluation masks and definitions should be independently audited before relying on scientific comparisons.

Research preprint: https://doi.org/10.5281/zenodo.24299509
