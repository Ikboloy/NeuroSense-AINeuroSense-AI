"""Run offline depth evaluations with independently obtained Middlebury files."""
import argparse
import csv
from pathlib import Path
import numpy as np
from .evaluation import read_pfm, read_middlebury_calibration, region_depth_metrics, depth_bin_metrics


def main(argv=None):
    p = argparse.ArgumentParser(description="NeuroSense AI offline depth metrics")
    p.add_argument("--prediction", type=Path, required=True, help="Predicted disparity .npy")
    p.add_argument("--reference", type=Path, required=True, help="Reference disparity .pfm")
    p.add_argument("--calibration", type=Path, required=True, help="Middlebury calib.txt")
    p.add_argument("--output", type=Path, required=True, help="Output CSV file")
    p.add_argument("--mode", choices=("scene","bins"), default="scene")
    args = p.parse_args(argv)
    pred = np.load(args.prediction, allow_pickle=False)
    gt = read_pfm(args.reference)
    fx, baseline_m, doffs = read_middlebury_calibration(args.calibration)
    if args.mode == "scene":
        rows = [dict(region="full_scene", **region_depth_metrics(pred,gt,fx,baseline_m,doffs))]
    else:
        rows = depth_bin_metrics(pred,gt,fx,baseline_m,doffs)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print("Saved:", args.output)


if __name__ == "__main__":
    main()
