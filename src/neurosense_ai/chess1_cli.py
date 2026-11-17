"""Run Chess1 experiments from the installable NeuroSense AI package."""
import argparse
from pathlib import Path
from .chess1 import evaluate_chess1, write_rows


def main(argv=None):
    p=argparse.ArgumentParser(description="Reproduce Chess1 confidence and near-surface metrics")
    p.add_argument("--scene",type=Path,required=True,help="Directory with im0.png, im1.png, disp0.pfm, calib.txt")
    p.add_argument("--output",type=Path,default=Path("results/chess1"))
    args=p.parse_args(argv)
    confidence,near=evaluate_chess1(args.scene)
    write_rows(args.output/"confidence_metrics.csv",confidence)
    write_rows(args.output/"near_surface_metrics.csv",near)
    for row in confidence+near: print(row)


if __name__=="__main__":
    main()
