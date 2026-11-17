"""Reproducible Chess1 experiments 14 and 16 (original numerical conventions)."""
from pathlib import Path
import csv
import numpy as np
import cv2
from .evaluation import read_pfm, read_middlebury_calibration


def compute_lr_disparities(left, right, ndisp, scale=0.5):
    """StereoSGBM settings reproduced from original experiment12.py."""
    h, w = left.shape
    size = (round(w*scale), round(h*scale))
    ls = cv2.resize(left, size, interpolation=cv2.INTER_AREA)
    rs = cv2.resize(right, size, interpolation=cv2.INTER_AREA)
    nd = max(16, ((int(np.ceil(ndisp*scale))+15)//16)*16)
    def matcher(min_disp):
        block = 9
        return cv2.StereoSGBM_create(
            minDisparity=min_disp, numDisparities=nd, blockSize=block,
            P1=8*block*block, P2=32*block*block,
            disp12MaxDiff=0, uniquenessRatio=10,
            speckleWindowSize=100, speckleRange=2,
            mode=cv2.STEREO_SGBM_MODE_SGBM)
    dl = matcher(0).compute(ls, rs).astype(np.float32)/16.0
    dr = matcher(-nd).compute(rs, ls).astype(np.float32)/16.0
    dl[~(dl>0)] = np.nan
    dr[~((dr>=-nd)&(dr<0))] = np.nan
    return dl, dr


def evaluate_chess1(folder, scale=0.5, lr_tolerance=1.0, near_threshold_m=1.5):
    """Return confidence and near-surface rows from Chess1 image pairs.

    Mirrors experiment14/16: LR consistency at reduced resolution;
    nearest-neighbour upsampling; <= for near threshold; >2px for Bad2.
    """
    folder = Path(folder)
    left = cv2.imread(str(folder/"im0.png"), cv2.IMREAD_GRAYSCALE)
    right = cv2.imread(str(folder/"im1.png"), cv2.IMREAD_GRAYSCALE)
    if left is None or right is None:
        raise FileNotFoundError("Missing Chess1 im0.png or im1.png")
    gt = read_pfm(folder/"disp0.pfm")
    if left.shape != right.shape or gt.shape != left.shape:
        raise ValueError("Chess1 image/reference shape mismatch")
    fx, baseline_m, doffs = read_middlebury_calibration(folder/"calib.txt")
    import re
    cal_text = (folder/"calib.txt").read_text(encoding="utf-8")
    m = re.search(r"^ndisp\s*=\s*(\d+)", cal_text, re.M)
    if not m:
        raise ValueError("Missing ndisp")
    dl, dr = compute_lr_disparities(left, right, int(m.group(1)), scale)
    yy, xx = np.indices(dl.shape)
    target = np.rint(np.where(np.isfinite(dl), xx-dl, -1)).astype(np.int32)
    inside = np.isfinite(dl)&(target>=0)&(target<dl.shape[1])
    sampled = np.full(dl.shape, np.nan, dtype=np.float32)
    sampled[inside] = dr[yy[inside],target[inside]]
    consistent_small = inside & np.isfinite(sampled) & (np.abs(dl+sampled)<=lr_tolerance)
    h,w = left.shape
    disp = cv2.resize(dl,(w,h),interpolation=cv2.INTER_NEAREST)/scale
    consistent = cv2.resize(consistent_small.astype(np.uint8),(w,h),interpolation=cv2.INTER_NEAREST).astype(bool)
    valid_gt = np.isfinite(gt)&(gt>0)
    valid_disp = np.isfinite(disp)&(disp>0)
    n_gt = int(valid_gt.sum())
    err = np.abs(disp-gt)
    confidence=[]
    def pct(n,d): return round(100*n/d,2) if d else float("nan")
    for state,mask in (
        ("VALID",valid_disp&consistent),
        ("UNCERTAIN",valid_disp&~consistent),
        ("INVALID",~valid_disp)):
        eligible=mask&valid_gt
        n=int(eligible.sum())
        confidence.append(dict(
            state=state,pixels_with_gt=n,share_of_gt_pct=pct(n,n_gt),
            mae_px=round(float(np.mean(err[eligible])),4) if n and state!="INVALID" else float("nan"),
            bad2_pct=pct(int((err[eligible]>2.0).sum()),n) if n and state!="INVALID" else float("nan")))
    with np.errstate(divide="ignore",invalid="ignore"):
        gt_depth=fx*baseline_m/(gt+doffs)
        pred_depth=fx*baseline_m/(disp+doffs)
    valid_gt_depth=valid_gt & np.isfinite(gt_depth)&(gt_depth>0)
    valid_pred=valid_disp&np.isfinite(pred_depth)&(pred_depth>0)
    gt_near=valid_gt_depth&(gt_depth<=near_threshold_m)
    pred_near=valid_pred&(pred_depth<=near_threshold_m)
    near=[]
    for name,alert,unknown in (
        ("BASELINE",pred_near,valid_gt_depth&~valid_pred),
        ("STRICT_LR",pred_near&consistent,valid_gt_depth&~(valid_pred&consistent)),
        ("CONFIDENCE_AWARE",pred_near&consistent,valid_gt_depth&~(valid_pred&consistent))):
        tp=int((alert&gt_near).sum())
        fn=int((~alert&gt_near).sum())
        fp=int((alert&valid_gt_depth&~gt_near).sum())
        recall=100*tp/(tp+fn) if tp+fn else float("nan")
        precision=100*tp/(tp+fp) if tp+fp else float("nan")
        near.append(dict(strategy=name,tp=tp,fn=fn,fp=fp,
                         recall_pct=round(recall,2),fnr_pct=round(100-recall,2),
                         precision_pct=round(precision,2),
                         unknown_pct=pct(int(unknown.sum()),int(valid_gt_depth.sum()))))
    return confidence,near


def write_rows(path,rows):
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
