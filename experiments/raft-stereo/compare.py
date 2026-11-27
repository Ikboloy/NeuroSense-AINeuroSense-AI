"""Compare official RAFT-Stereo demo --save_numpy output with SGBM.
Usage: python compare.py SCENE RAFT_FLOW.npy OUTPUT_DIR
SCENE: full-resolution rectified im0.png, im1.png and calib.txt; optional disp0.pfm.
"""
import argparse
import json
import re
from pathlib import Path
from time import perf_counter

import cv2
import numpy as np


def read_middlebury_disparity(path):
    """Read Middlebury pixel disparities; magnitude of PFM scale is not a disparity multiplier."""
    with path.open("rb") as stream:
        if stream.readline().strip() != b"Pf":
            raise ValueError("Expected grayscale PFM")
        w, h = map(int, stream.readline().split())
        scale = float(stream.readline())
        if w <= 0 or h <= 0 or not np.isfinite(scale) or scale == 0:
            raise ValueError("Invalid PFM header")
        data = np.fromfile(stream, dtype="<f4" if scale < 0 else ">f4")
        return np.flipud(data.reshape(h, w)).copy()


def compare(scene, flow_path, out):
    left, right = [cv2.imread(str(scene / name), cv2.IMREAD_GRAYSCALE)
                   for name in ("im0.png", "im1.png")]
    if left is None or right is None or left.shape != right.shape:
        raise ValueError("Expected matching rectified grayscale image dimensions")
    raft = -np.load(flow_path, allow_pickle=False)  # upstream saves signed horizontal flow
    if raft.shape != left.shape:
        raise ValueError("RAFT flow must match the original image resolution")
    raw = int(re.search(r"(?m)^ndisp\s*=\s*(\d+)", (scene / "calib.txt").read_text())[1])
    n = ((raw + 15) // 16) * 16
    matcher = cv2.StereoSGBM_create(minDisparity=0, numDisparities=n, blockSize=5,
                                    P1=200, P2=800, uniquenessRatio=10)
    start = perf_counter()
    sgbm = matcher.compute(left, right).astype(np.float32) / 16
    stats = {"sgbm_seconds": perf_counter() - start, "num_disparities": n}
    maps = {"sgbm": sgbm, "raft": raft}
    masks = {k: np.isfinite(v) & (v >= 0) for k, v in maps.items()}
    stats["coverage_fraction"] = {k: float(m.mean()) for k, m in masks.items()}
    if (scene / "disp0.pfm").exists():
        gt = read_middlebury_disparity(scene / "disp0.pfm")
        if gt is None or gt.shape != left.shape:
            raise ValueError("Invalid ground truth")
        common = masks["sgbm"] & masks["raft"] & np.isfinite(gt) & (gt >= 0)
        stats["common_pixels"] = int(common.sum())
        if common.any():
            for k, v in maps.items():
                err = np.abs(v[common] - gt[common])
                stats[k] = {"mae_px": float(err.mean()), "bad2_fraction": float((err > 2).mean())}
    panels = [cv2.cvtColor(left, cv2.COLOR_GRAY2BGR)]
    for k, v in maps.items():
        scaled = np.clip(np.where(masks[k], v, 0) / n, 0, 1)
        panel = cv2.applyColorMap((255 * scaled).astype("uint8"), cv2.COLORMAP_TURBO)
        panel[~masks[k]] = 0
        panels.append(panel)
    out.mkdir(exist_ok=True, parents=True)
    if not cv2.imwrite(str(out / "left-sgbm-raft.png"), np.hstack(panels)):
        raise IOError("Could not write comparison")
    (out / "metrics.json").write_text(json.dumps(stats, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("scene", "flow_path", "out"):
        p.add_argument(name, type=Path)
    compare(**vars(p.parse_args()))
