# Reproducible 3D point-cloud generation

`neurosense_ai.pointcloud` extracts the core geometry from the author's original `reconstruct3d.py`. It uses a rectified pinhole stereo model:

- `Z = fx * baseline_m / (disparity_px + doffs_px)`
- `X = (u - cx) * Z / fx`
- `Y = (v - cy) * Z / fy`

It samples every fourth pixel by default, filters nonpositive/nonfinite disparities, and retains depths between 0.2 and 20 metres. Coordinates are in metres. Colors must be **RGB**, not OpenCV BGR.

## Example

```python
import cv2
import numpy as np
from neurosense_ai.pointcloud import disparity_to_points, write_ply

image_bgr = cv2.imread("dataset/scene1/im0.png")
rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
disp = np.load("results_272/sgbm_disparity.npy")
# Values below are examples ONLY; replace with actual calibrated fx/fy/cx/cy/baseline/doffs.
points, colors = disparity_to_points(disp, rgb, fx=1000, fy=1000,
    cx=rgb.shape[1]/2, cy=rgb.shape[0]/2, baseline_m=0.1, doffs=0)
write_ply("results/pointcloud.ply", points, colors)
```

For scientific reproduction, read camera parameters from the actual Middlebury `calib.txt`, not the illustrative values above.

## Validation status

Synthetic geometry and PLY serialization are covered by unit tests. **Exact point-by-point comparison to the original Motorcycle `neurosense_pointcloud.ply` has not yet been performed.** The point cloud is an offline research visualization, not a navigation system.
