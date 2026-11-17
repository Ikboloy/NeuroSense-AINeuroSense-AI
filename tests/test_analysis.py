import numpy as np
import pytest

from neurosense_ai import (
    disparity_to_depth, left_right_consistency,
    disparity_error, near_surface_metrics,
)


def test_depth_conversion():
    result = disparity_to_depth(np.array([4.0, 8.0]), 100.0, 0.1)
    assert np.allclose(result, [2.5, 1.25])


def test_depth_invalid():
    result = disparity_to_depth(np.array([0.0, -1.0, np.nan]), 100.0, 0.1)
    assert np.isnan(result).all()


def test_depth_offset():
    assert np.isclose(disparity_to_depth([5], 100, 0.1, doffs=5)[0], 1.0)


def test_depth_bad_calibration():
    with pytest.raises(ValueError):
        disparity_to_depth([2], 0, 0.1)


def test_consistency_signed_right():
    left = np.array([[0.0, 1.0, 2.0]])
    right = np.array([[-1.0, 0.0, 0.0]])
    assert np.array_equal(left_right_consistency(left, right), [[False, True, False]])


def test_consistency_shape():
    with pytest.raises(ValueError):
        left_right_consistency(np.ones((2, 2)), np.ones((2, 3)))


def test_disparity_error():
    result = disparity_error([1, 4, np.nan], [1, 2, 3])
    assert result["evaluated"] == 2
    assert np.isclose(result["mae_px"], 1)
    assert np.isclose(result["coverage_pct"], 200 / 3)


def test_disparity_valid_mask():
    result = disparity_error([1, 10], [1, 2], valid_mask=[True, False])
    assert result["evaluated"] == 1
    assert result["bad_pct"] == 0


def test_near_surface():
    result = near_surface_metrics([1.0, 1.0, np.nan], [1.0, 2.0, 1.0])
    assert (result["tp"], result["fn"], result["fp"]) == (1, 1, 1)
    assert np.isclose(result["recall"], 0.5)
    assert np.isclose(result["unknown_pct"], 100 / 3)
