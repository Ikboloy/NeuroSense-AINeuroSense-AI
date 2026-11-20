# Motorcycle stereo confidence experiment

Run `python -m pip install numpy scipy pillow`, then `python bench.py path/to/Motorcycle*.zip > results.csv` with the two Motorcycle archives in that directory. Raw data are not redistributed.

At quarter resolution a 5×5 grayscale block matcher searches the calibrated disparity range. LR retains positive estimates consistent in both directions within one pixel. Numeric rows additionally require the runner-up matching cost minus the best to exceed the threshold. Coverage uses finite positive reference disparity in the interior evaluation region; MAE is measured only on retained pixels, in resized-image disparity pixels. The two variants depict the same scene; these measurements do not establish generalization.
