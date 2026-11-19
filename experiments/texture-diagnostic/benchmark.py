"""Controlled planar stereo diagnostic. Run inside this directory."""
import csv
import time
import platform
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(47)
h, w, d = 96, 192, 6
# Mean SAD in 5x5 windows; search integer disparities 0..12.
def match(a, b, direction):
    costs = []
    for k in range(13):
        v = np.abs(a.astype(float) - np.roll(b, direction*k, axis=1))
        z = np.pad(v, 2, mode="edge")
        costs.append(np.lib.stride_tricks.sliding_window_view(z, (5,5)).mean(axis=(-1,-2)))
    return np.argmin(costs, axis=0)

fig, axes = plt.subplots(3, 3, figsize=(9,5))
rows = []
x = np.indices((h,w))[1]
for i, name in enumerate(["Random texture", "Blank center", "Repeated stripes"]):
    a = rng.integers(0,256,(h,w),dtype=np.uint8)
    if i == 1: a[20:78,50:146] = 128
    if i == 2: a = ((x % 4 < 2)*200).astype(np.uint8)
    b = np.roll(a,-d,axis=1)
    b[:,-d:] = 0
    times = []
    for _ in range(5):
        t = time.perf_counter()
        left, right = match(a,b,1), match(b,a,-1)
        keep = (left > 0) & (abs(left - np.take_along_axis(right,np.maximum(x-left,0),axis=1)) <= 1)
        times.append(1000*(time.perf_counter()-t))
    roi = (x>=26)&(x<w-26)
    valid = roi & keep
    err = abs(left-d)
    rows.append([name,round(err[roi].mean(),3),round(100*valid.sum()/roi.sum(),2),round(err[valid].mean(),3) if valid.any() else None,round(np.median(times),1)])
    for ax,img in zip(axes[i],[a,err,valid]):
        ax.imshow(img,cmap="gray",vmin=0,vmax=255 if ax==axes[i,0] else (12 if ax==axes[i,1] else 1))
        ax.set_xticks([]); ax.set_yticks([])
    axes[i,0].set_ylabel(name)
for ax,title in zip(axes[0],["Left image","Error (0–12 px)","Retained (white)"]): ax.set_title(title)
fig.tight_layout()
fig.savefig("comparison.svg",dpi=85)
with open("results.csv","w",newline="") as f:
    writer=csv.writer(f);writer.writerow(["scene","raw_MAE_px","coverage_pct","retained_MAE_px","median_ms"]);writer.writerows(rows)
print(rows, platform.machine(), np.__version__)
