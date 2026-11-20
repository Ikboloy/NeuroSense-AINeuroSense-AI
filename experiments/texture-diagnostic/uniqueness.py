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
    best_two = np.partition(costs, 1, axis=0)[:2]
    return np.argmin(costs, axis=0), best_two[1] - best_two[0]

fig, axes = plt.subplots(3, 3, figsize=(9,5))
rows = []
x = np.indices((h,w))[1]
for i, name in enumerate(["Random texture", "Blank center", "Repeated stripes"]):
    a = rng.integers(0,256,(h,w),dtype=np.uint8)
    if i == 1: a[20:78,50:146] = 128
    if i == 2: a = ((x % 4 < 2)*200).astype(np.uint8)
    b = np.roll(a,-d,axis=1)
    b[:,-d:] = 0
    left, gap = match(a,b,1)
    right, _ = match(b,a,-1)
    roi = (x>=26)&(x<w-26)
    lr = roi & (left>0) & (abs(left-np.take_along_axis(right,np.maximum(x-left,0),axis=1))<=1)
    unique = lr & (gap>0)  # exact ties only; not calibrated confidence
    for label,mask in [("LR",lr),("LR + unique",unique)]:
        rows.append([name,label,int(mask.sum()),int(roi.sum()),round(100*mask.sum()/roi.sum(),2), round(abs(left[mask]-d).mean(),4) if mask.any() else "NA"])
    for ax,img in zip(axes[i],[a,lr,unique]):
        ax.imshow(img[:,26:-26], cmap="gray",vmin=0,vmax=255 if ax==axes[i,0] else 1)
        ax.set_xticks([]); ax.set_yticks([])
    axes[i,0].set_ylabel(name)
for ax,title in zip(axes[0],["Left image","LR retained","LR + unique retained"]): ax.set_title(title)
fig.tight_layout()
fig.savefig("uniqueness.png",dpi=100)
with open("uniqueness.csv","w",newline="") as f:
    writer=csv.writer(f);writer.writerow(["scene","filter","kept","evaluated","coverage_pct","retained_MAE_px"]);writer.writerows(rows)
