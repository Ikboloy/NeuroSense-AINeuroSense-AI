# When consistent stereo is wrong

![Three synthetic stereo conditions: input, absolute disparity error and retained pixels](comparison.svg)

These are controlled synthetic planes at 6 px disparity, not Middlebury scenes or a navigation evaluation. This standalone NumPy SAD baseline is separate from the package's Chess1 pipeline. Repeated stripes admit several equally good matches. Both views choose disparity 2 instead of 6: every evaluated pixel passes consistency despite a 4 px error.

[Measured CSV](results.csv) · [Generator and evaluation](benchmark.py)

Run `python benchmark.py` in this folder with NumPy and Matplotlib installed. Coverage is the retained fraction of the interior ROI (26 columns excluded per side). Positive disparities with left/right difference ≤1 px are retained. MAE is disparity error in pixels, not metric depth error. Timing is the median of five runs of both matchers and the filter, excluding data generation and plotting (x86_64, NumPy 2.3.5). It is not a device latency prediction.
