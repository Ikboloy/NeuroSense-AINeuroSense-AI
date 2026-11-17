import numpy as np
import pytest
from neurosense_ai.evaluation import (
    read_pfm, read_middlebury_calibration, region_depth_metrics, depth_bin_metrics
)


def test_region_metrics_and_coverage():
    gt = np.array([[2.0, 2.0, 0.0]])
    pred = np.array([[2.0, -1.0, 1.0]])
    m = region_depth_metrics(pred, gt, 100, 0.1, 0)
    assert m["gt_valid_pixels"] == 2
    assert m["common_valid_pixels"] == 1
    assert m["coverage_pct"] == 50
    assert m["depth_mae_m"] == 0


def test_depth_bins():
    gt = np.array([[5.0, 2.5, 0.0]])
    pred = np.array([[5.0, 2.5, -1.0]])
    rows = depth_bin_metrics(pred, gt, 100, 0.1, 0, bins=((0,3),(3,5)))
    assert [r["common_valid_pixels"] for r in rows] == [1,1]


def test_shape_validation():
    with pytest.raises(ValueError):
        region_depth_metrics(np.ones((2,)), np.ones((3,)), 100, 0.1, 0)


def test_pfm_roundtrip(tmp_path):
    p = tmp_path / "ref.pfm"
    import struct
    with p.open("wb") as f:
        f.write(b"Pf\n2 2\n-1.0\n")
        f.write(struct.pack("<4f",3,4,1,2))
    assert np.array_equal(read_pfm(p), [[1,2],[3,4]])


def test_calibration(tmp_path):
    p = tmp_path / "calib.txt"
    p.write_text("cam0=[100 0 1; 0 100 1; 0 0 1]\nbaseline=200\ndoffs=5\n")
    assert read_middlebury_calibration(p) == (100.0,0.2,5.0)
