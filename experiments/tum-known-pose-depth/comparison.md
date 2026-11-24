# Does the stereo matching-cost margin transfer to video depth?

Run `python compare.py /path/to/rgbd_dataset_freiburg1_xyz > comparison.csv` with NumPy, SciPy and Pillow. See [the baseline protocol](README.md) and [all measurements](comparison.csv). Baseline counts and pooled metrics reproduce the previous run at reported precision.

Before consulting sensor depths, subtract the minimum cost from the second-lowest cost across the 80 inverse-depth planes. Keep gaps strictly above 0, 1 or 3 grayscale units (numerical tolerance 1e-8). Reference depths are used for scoring and defining the common evaluation region only. We transfer the gap rule, not the stereo left-right check. Adjacent depth planes can produce almost identical image shifts, so the gap measures separation on this particular sampling grid.

Gap >1 retained 7,097/130,422 scored pixels (5.44%); retained median error fell from 15.64 to 11.06 cm. Gap >3 retained 755 pixels and raised mean error from 38.05 to 52.38 cm. Errors are conditional on retention: no depth values were corrected. These results from ten frame pairs on one desk scene do not establish reliable obstacle detection.