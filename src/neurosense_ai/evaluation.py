"""Offline Middlebury-style depth evaluation adapted from original experiments 19B/20.

The original scripts use reference PFM disparity, predicted NPY disparity and
Middlebury calibration parameters (fx, baseline, doffs).
"""
from pathlib import Path
import re
import numpy as np


def read_pfm(path):
    """Read a single-channel PFM disparity map in bottom-to-top file order."""
    with Path(path).open("rb") as f:
        header = f.readline().strip()
        if header != b"Pf":
            raise ValueError("Expected grayscale PFM (Pf)")
        dimensions = f.readline().decode("ascii").strip()
        while dimensions.startswith("#"):
            dimensions = f.readline().decode("ascii").strip()
        width, height = map(int, dimensions.split())
        scale = float(f.readline().strip())
        if not np.isfinite(scale) or scale == 0:
            raise ValueError("Invalid PFM scale")
        dtype = "<f4" if scale < 0 else ">f4"
        values = np.fromfile(f, dtype=dtype, count=width * height)
        if values.size != width * height:
            raise ValueError("Truncated PFM")
    return np.flipud(values.reshape(height, width)).copy()


def read_middlebury_calibration(path):
    """Read fx (pixels), baseline (metres) and doffs (pixels)."""
    data = Path(path).read_text(encoding="utf-8")
    cam = re.search(r"^cam0=\[([^\]]+)\]", data, re.M)
    if not cam:
        raise ValueError("Missing cam0")
    fx = float(cam.group(1).split(";")[0].split()[0])
    def scalar(key):
        match = re.search(r"^" + re.escape(key) + r"=([^\r\n]+)", data, re.M)
        if not match:
            raise ValueError("Missing " + key)
        return float(match.group(1))
    baseline_m = scalar("baseline") / 1000.0
    doffs = scalar("doffs")
    if not (np.isfinite(fx) and fx > 0 and np.isfinite(baseline_m) and baseline_m > 0 and np.isfinite(doffs)):
        raise ValueError("Invalid calibration")
    return fx, baseline_m, doffs


def _valid(d, doffs):
    return np.isfinite(d) & (d > 0) & (d + doffs > 0)


def region_depth_metrics(prediction, reference, fx, baseline_m, doffs, region=None):
    """Reproduce original experiment19b region-level definitions."""
    pred = np.asarray(prediction, dtype=float)
    gt = np.asarray(reference, dtype=float)
    if pred.shape != gt.shape:
        raise ValueError("Shape mismatch")
    if region is None:
        region = np.ones(gt.shape, dtype=bool)
    region = np.asarray(region, dtype=bool)
    if region.shape != gt.shape:
        raise ValueError("Region shape mismatch")
    eligible = _valid(gt, doffs) & region
    common = eligible & _valid(pred, doffs)
    n_gt, n = int(eligible.sum()), int(common.sum())
    if not n:
        return dict(gt_valid_pixels=n_gt, common_valid_pixels=0,
                    coverage_pct=(100*n/n_gt if n_gt else float("nan")),
                    disparity_mae_px=float("nan"), depth_mae_m=float("nan"))
    dgt, dp = gt[common], pred[common]
    errors = np.abs(fx*baseline_m/(dp+doffs) - fx*baseline_m/(dgt+doffs))
    return dict(gt_valid_pixels=n_gt, common_valid_pixels=n,
                coverage_pct=100*n/n_gt,
                disparity_mae_px=float(np.abs(dp-dgt).mean()),
                depth_mae_m=float(errors.mean()))


def depth_bin_metrics(prediction, reference, fx, baseline_m, doffs,
                      bins=((0,1),(1,2),(2,3),(3,5),(5,20))):
    """Reproduce original experiment20 depth-bin definitions."""
    pred = np.asarray(prediction, dtype=float)
    gt = np.asarray(reference, dtype=float)
    if pred.shape != gt.shape:
        raise ValueError("Shape mismatch")
    valid_gt = _valid(gt, doffs)
    valid_pred = _valid(pred, doffs)
    z_gt = np.full(gt.shape, np.nan)
    z_gt[valid_gt] = fx*baseline_m/(gt[valid_gt]+doffs)
    rows = []
    for low, high in bins:
        region = valid_gt & (z_gt >= low) & (z_gt < high)
        common = region & valid_pred
        n_gt, n = int(region.sum()), int(common.sum())
        row = dict(distance_range=f"{low:g}-{high:g}m", gt_valid_pixels=n_gt,
                   common_valid_pixels=n,
                   coverage_pct=100*n/n_gt if n_gt else float("nan"),
                   depth_mae_m=float("nan"), depth_p95_m=float("nan"),
                   disparity_mae_px=float("nan"))
        if n:
            dz = np.abs(fx*baseline_m/(pred[common]+doffs)-z_gt[common])
            row.update(depth_mae_m=float(dz.mean()),
                       depth_p95_m=float(np.percentile(dz,95)),
                       disparity_mae_px=float(np.abs(pred[common]-gt[common]).mean()))
        rows.append(row)
    return rows
