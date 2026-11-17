"""Optional regression against original Motorcycle PLY, using user-provided data.

Environment:
 NEUROSENSE_MOTORCYCLE_DIR directory containing im0.png, calib.txt,
 sgbm_disparity.npy and archived_pointcloud.ply.
"""
import os
import re
from pathlib import Path
import numpy as np
import pytest

from neurosense_ai.pointcloud import disparity_to_points

ROOT = os.environ.get("NEUROSENSE_MOTORCYCLE_DIR")
pytestmark = pytest.mark.skipif(not ROOT, reason="Motorcycle original dataset/PLY not provided")


def test_original_motorcycle_pointcloud():
    cv2 = pytest.importorskip("cv2")
    root = Path(ROOT)
    calib = (root / "calib.txt").read_text()
    cam = re.search(r"^cam0=\[([^\]]+)\]", calib, re.M)
    assert cam is not None
    k = np.array([[float(v) for v in line.split()] for line in cam.group(1).split(";")])
    baseline_m = float(re.search(r"^baseline=([^\r\n]+)", calib, re.M).group(1)) / 1000.0
    doffs = float(re.search(r"^doffs=([^\r\n]+)", calib, re.M).group(1))
    bgr = cv2.imread(str(root / "im0.png"))
    assert bgr is not None
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    disparity = np.load(root / "sgbm_disparity.npy", allow_pickle=False)
    points, colors = disparity_to_points(
        disparity, rgb, k[0,0], k[1,1], k[0,2], k[1,2],
        baseline_m, doffs, step=4)
    archived = np.loadtxt(root / "archived_pointcloud.ply", skiprows=10)
    assert points.shape == (301197, 3)
    assert archived.shape == (301197, 6)
    assert np.allclose(points, archived[:,:3], rtol=0, atol=1e-5)
    np.testing.assert_array_equal(colors, archived[:,3:].astype(np.uint8))
