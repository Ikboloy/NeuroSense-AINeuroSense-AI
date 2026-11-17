"""Optional full-data regression test for archived Chess1 experiments.

Set NEUROSENSE_CHESS1_DIR to a locally obtained Middlebury Chess1 directory.
The public CI does not bundle copyrighted/third-party image data.
"""
import math
import os
from pathlib import Path
import pytest

from neurosense_ai.chess1 import evaluate_chess1

SCENE = os.environ.get("NEUROSENSE_CHESS1_DIR")
pytestmark = pytest.mark.skipif(
    not SCENE, reason="Set NEUROSENSE_CHESS1_DIR for full-data regression"
)

EXPECTED_CONFIDENCE = [
    ("VALID", 1024634, 57.97, 4.1764, 24.35),
    ("UNCERTAIN", 274671, 15.54, 13.9023, 36.05),
    ("INVALID", 468231, 26.49, float("nan"), float("nan")),
]
EXPECTED_NEAR = [
    ("BASELINE", 922679, 146303, 44658, 86.31, 13.69, 95.38, 26.49),
    ("STRICT_LR", 746849, 322133, 29609, 69.87, 30.13, 96.19, 42.03),
    ("CONFIDENCE_AWARE", 746849, 322133, 29609, 69.87, 30.13, 96.19, 42.03),
]


def test_chess1_archived_metrics():
    scene = Path(SCENE)
    for filename in ("im0.png", "im1.png", "disp0.pfm", "calib.txt"):
        assert (scene / filename).is_file(), f"Missing {filename}"
    confidence, near = evaluate_chess1(scene)
    assert len(confidence) == 3
    assert len(near) == 3
    for row, expected in zip(confidence, EXPECTED_CONFIDENCE):
        actual = (row["state"], row["pixels_with_gt"], row["share_of_gt_pct"],
                  row["mae_px"], row["bad2_pct"])
        for got, want in zip(actual, expected):
            assert got == want or (isinstance(want, float) and math.isnan(want) and math.isnan(got)), (row, expected)
    for row, expected in zip(near, EXPECTED_NEAR):
        actual = tuple(row[key] for key in (
            "strategy", "tp", "fn", "fp", "recall_pct", "fnr_pct",
            "precision_pct", "unknown_pct"))
        assert actual == expected, (row, expected)
