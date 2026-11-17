"""Metric RGB point-cloud reconstruction from calibrated stereo disparity."""
from pathlib import Path
import numpy as np


def disparity_to_points(disparity, rgb, fx, fy, cx, cy, baseline_m,
                        doffs=0.0, step=4, min_depth_m=0.2, max_depth_m=20.0):
    """Return (N,3) XYZ metres and (N,3) uint8 RGB arrays.

    Refactors the equations and filtering in the original reconstruct3d.py.
    Coordinates use the original full-resolution pixel indices even when sampled.
    """
    d = np.asarray(disparity)
    image = np.asarray(rgb)
    if d.ndim != 2 or image.shape != (*d.shape, 3):
        raise ValueError("Expected HxW disparity and HxWx3 RGB image")
    if not isinstance(step, int) or step < 1:
        raise ValueError("step must be a positive integer")
    if not all(np.isfinite(v) for v in (fx, fy, cx, cy, baseline_m, doffs)):
        raise ValueError("Calibration must be finite")
    if fx <= 0 or fy <= 0 or baseline_m <= 0 or min_depth_m < 0 or max_depth_m <= min_depth_m:
        raise ValueError("Invalid calibration or depth limits")
    sample = d[::step, ::step].astype(np.float64)
    colors = image[::step, ::step]
    v, u = np.mgrid[0:d.shape[0]:step, 0:d.shape[1]:step]
    denom = sample + doffs
    valid = np.isfinite(sample) & (sample > 0) & (denom > 0)
    z = np.full(sample.shape, np.nan, dtype=np.float64)
    z[valid] = fx * baseline_m / denom[valid]
    valid &= np.isfinite(z) & (z >= min_depth_m) & (z <= max_depth_m)
    x = (u[valid] - cx) * z[valid] / fx
    y = (v[valid] - cy) * z[valid] / fy
    points = np.column_stack((x, y, z[valid]))
    return points, colors[valid].astype(np.uint8)


def write_ply(path, points, colors):
    """Save ASCII PLY, matching the original XYZ+RGB schema."""
    xyz = np.asarray(points)
    rgb = np.asarray(colors)
    if xyz.ndim != 2 or xyz.shape[1] != 3 or rgb.shape != xyz.shape:
        raise ValueError("Expected matching Nx3 point and color arrays")
    if not np.isfinite(xyz).all():
        raise ValueError("Non-finite 3D point")
    if np.any((rgb < 0) | (rgb > 255)):
        raise ValueError("RGB outside 0..255")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii") as f:
        f.write("ply\nformat ascii 1.0\n")
        f.write(f"element vertex {len(xyz)}\n")
        f.write("property float x\nproperty float y\nproperty float z\n")
        f.write("property uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n")
        for p, c in zip(xyz, rgb):
            f.write(f"{p[0]:.5f} {p[1]:.5f} {p[2]:.5f} {int(c[0])} {int(c[1])} {int(c[2])}\n")
