"""Reusable offline stereo analysis.

These are independent utilities, not a complete reproduction of the preprint.
Rejected estimates are unknown, not confirmed free space.
"""
import numpy as np


def disparity_to_depth(disparity, focal_px, baseline_m, doffs=0.0):
    """Calculate depth (metres) using Z = f B / (d + doffs).

    Pixels with invalid/nonpositive disparity or denominator yield NaN.
    """
    d = np.asarray(disparity, dtype=float)
    if not np.isfinite(focal_px) or focal_px <= 0:
        raise ValueError("focal_px must be finite and positive")
    if not np.isfinite(baseline_m) or baseline_m <= 0:
        raise ValueError("baseline_m must be finite and positive")
    if not np.isfinite(doffs):
        raise ValueError("doffs must be finite")
    denom = d + doffs
    valid = np.isfinite(d) & (d > 0) & (denom > 0)
    result = np.full(d.shape, np.nan, dtype=float)
    np.divide(focal_px * baseline_m, denom, out=result, where=valid)
    return result


def left_right_consistency(left_disparity, right_disparity, tolerance_px=1.0):
    """Check LR consistency for *signed* right disparity.

    Convention: right-map disparities are negative. Correspondence x_r=x_l-d_l,
    and consistency requires abs(d_l+d_r(x_r)) <= tolerance_px.
    Rejected/out-of-bounds pixels are False.
    """
    left = np.asarray(left_disparity, dtype=float)
    right = np.asarray(right_disparity, dtype=float)
    if left.ndim != 2 or left.shape != right.shape:
        raise ValueError("left/right disparities must be 2D and the same shape")
    if not np.isfinite(tolerance_px) or tolerance_px < 0:
        raise ValueError("tolerance_px must be nonnegative and finite")
    y, x = np.indices(left.shape)
    safe_d = np.where(np.isfinite(left), left, 0)
    right_x = np.rint(x - safe_d).astype(np.int64)
    inside = (right_x >= 0) & (right_x < left.shape[1])
    match = right[y, np.clip(right_x, 0, left.shape[1] - 1)]
    return (np.isfinite(left) & (left > 0) & inside
            & np.isfinite(match) & (np.abs(left + match) <= tolerance_px))


def disparity_error(prediction, reference, valid_mask=None, bad_threshold_px=2.0):
    """Compute disparity errors on valid prediction/reference intersections.

    Coverage denominator is the number of positive, finite reference pixels.
    """
    predicted = np.asarray(prediction, dtype=float)
    gt = np.asarray(reference, dtype=float)
    if predicted.shape != gt.shape:
        raise ValueError("prediction/reference shapes differ")
    if not np.isfinite(bad_threshold_px) or bad_threshold_px < 0:
        raise ValueError("bad_threshold_px must be nonnegative and finite")
    reference_valid = np.isfinite(gt) & (gt > 0)
    common = reference_valid & np.isfinite(predicted) & (predicted > 0)
    if valid_mask is not None:
        mask = np.asarray(valid_mask, dtype=bool)
        if mask.shape != gt.shape:
            raise ValueError("valid_mask shape differs")
        common &= mask
    ref_n = int(reference_valid.sum())
    n = int(common.sum())
    abs_err = np.abs(predicted[common] - gt[common])
    return {
        "reference_valid": ref_n,
        "evaluated": n,
        "coverage_pct": float(100.0 * n / ref_n) if ref_n else float("nan"),
        "mae_px": float(abs_err.mean()) if n else float("nan"),
        "bad_pct": float(100.0 * np.mean(abs_err > bad_threshold_px)) if n else float("nan"),
    }


def near_surface_metrics(predicted_depth, reference_depth, threshold_m=1.5):
    """Measure recall and precision of near-surface predictions.

    Reference-valid pixels are finite and >0. An unavailable prediction
    cannot generate TP/FP; if the reference pixel is near, it counts as FN.
    """
    pred = np.asarray(predicted_depth, dtype=float)
    ref = np.asarray(reference_depth, dtype=float)
    if pred.shape != ref.shape:
        raise ValueError("prediction/reference shapes differ")
    if not np.isfinite(threshold_m) or threshold_m <= 0:
        raise ValueError("threshold_m must be finite and positive")
    reference_valid = np.isfinite(ref) & (ref > 0)
    predicted_valid = np.isfinite(pred) & (pred > 0)
    ref_near = reference_valid & (ref < threshold_m)
    pred_near = reference_valid & predicted_valid & (pred < threshold_m)
    tp = int(np.sum(ref_near & pred_near))
    fn = int(np.sum(ref_near & ~pred_near))
    fp = int(np.sum(~ref_near & pred_near))
    unknown = int(np.sum(reference_valid & ~predicted_valid))
    ref_n = int(reference_valid.sum())
    return {
        "tp": tp,
        "fn": fn,
        "fp": fp,
        "recall": tp / (tp + fn) if tp + fn else float("nan"),
        "precision": tp / (tp + fp) if tp + fp else float("nan"),
        "unknown_pct": 100.0 * unknown / ref_n if ref_n else float("nan"),
    }
