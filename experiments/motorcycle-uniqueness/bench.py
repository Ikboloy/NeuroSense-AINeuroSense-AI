"""Run: python bench.py path/to/Motorcycle*.zip (pass both archives)."""
import csv, io, sys, zipfile
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import uniform_filter

def match(a,b,sign,limit):
    best=np.full(a.shape,np.inf); second=best.copy(); disp=np.zeros(a.shape,int)
    for k in range(limit+1):
        cost=uniform_filter(abs(a-np.roll(b,sign*k,axis=1)),5)
        win=cost<best
        second=np.minimum(second,np.where(win,best,cost))
        best=np.minimum(best,cost); disp[win]=k
    return disp,second-best

def run(file):
    with zipfile.ZipFile(file) as z:
        prefix=next(n[:-9] for n in z.namelist() if n.endswith("calib.txt"))
        get=lambda n:z.read(prefix+n)
        def gray(n):
            im=Image.open(io.BytesIO(get(n))).convert("L")
            return np.asarray(im.resize((im.width//4,im.height//4),Image.Resampling.BOX),float)
        a,b=gray("im0.png"),gray("im1.png")
        f=io.BytesIO(get("disp0.pfm")); assert f.readline().strip()==b"Pf"
        w,h=map(int,f.readline().split()); scale=float(f.readline())
        gt=np.frombuffer(f.read(),dtype="<f4" if scale<0 else ">f4").reshape(h,w)[::-1]
        H,W=a.shape; ratio=W/w
        gt=gt[((np.arange(H)+.5)*h/H).astype(int)[:,None],((np.arange(W)+.5)*w/W).astype(int)]*ratio
        nd=int(next(s.split("=")[1] for s in get("calib.txt").decode().splitlines() if s.startswith("ndisp=")))
        limit=int(np.ceil(nd*ratio)); l,gap=match(a,b,1,limit); r,_=match(b,a,-1,limit)
        x=np.indices(a.shape)[1]; roi=np.isfinite(gt)&(gt>0)&(x>=limit+2)&(x<W-limit-2)
        keep=roi&(l>0)&(abs(l-np.take_along_axis(r,np.maximum(x-l,0),axis=1))<=1)
        for threshold in [None,0,1,3]:
            m=keep if threshold is None else keep&(gap>threshold+1e-8)
            yield [prefix.strip("/"),W,H,"LR" if threshold is None else threshold,int(roi.sum()),int(m.sum()),round(100*m.sum()/roi.sum(),2),round(abs(l[m]-gt[m]).mean(),3) if m.any() else "NA"]
if __name__=="__main__":
    out=csv.writer(sys.stdout);out.writerow("scene width height min_gap eligible kept coverage_pct mae_downsampled_px".split())
    for file in sys.argv[1:]:out.writerows(run(file))
