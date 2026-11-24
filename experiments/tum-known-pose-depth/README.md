# How accurately can two video frames recover desk-scene depth?

On ten frame pairs from TUM RGB-D **freiburg1_xyz**, the median absolute depth error was **15.6 cm**. Mean absolute error was **38.1 cm**; **38.2%** of evaluated pixels were within 10 cm of the depth sensor. These are pooled metrics from the original run, not averages of the per-pair medians in [pairs.csv](pairs.csv).

## What the experiment used

The estimator used grayscale images resized to 160 × 120 and **reference camera poses** from the dataset. It projected 80 inverse-depth candidates spanning 0.45–3 m into the second image, comparing brightness using a 5 × 5 window. Pairs were chosen from the next 24 frames to approximate a 6 cm camera displacement; displacements below 2.5 cm were excluded. Reference indices start at zero in timestamp order.

The nearest sensor depth frame (within 22 ms) was used for scoring. Evaluation excluded the six-pixel border, out-of-range sensor depths and pixels with minimum matching cost of 80 or greater. The ten pair counts sum to 130,422; the count is pixel observations, not independent physical points.

## What the result does and does not show

Pair medians ranged from 4.6 to 52.7 cm in this single sequence. Metric scale came from the supplied camera poses. This does not validate metric depth from an uncalibrated phone video or establish navigation safety. Results transcribed from the original experiment; no new run is claimed here.

Dataset: [TUM RGB-D benchmark](https://cvg.cit.tum.de/data/datasets/rgbd-dataset/download), Sturm et al., *A Benchmark for the Evaluation of RGB-D SLAM Systems* (IROS 2012).
