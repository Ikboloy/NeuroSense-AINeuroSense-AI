"""Usage: python compare.py PATH_TO_EXTRACTED_freiburg1_xyz > comparison.csv"""
import sys,csv
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates,uniform_filter
from scipy.spatial.transform import Rotation

p=Path(sys.argv[1])
rgb=sorted((p/'rgb').glob('*.png')); depth=sorted((p/'depth').glob('*.png'))
def timestamps(files): return np.array([float(f.stem) for f in files])
t,td=timestamps(rgb),timestamps(depth)
poses=np.loadtxt(p/'groundtruth.txt')
def pose(i):
    row=poses[np.argmin(abs(poses[:,0]-t[i]))]
    return Rotation.from_quat(row[4:]).as_matrix(),row[1:4]
def gray(i):
    return np.asarray(Image.open(rgb[i]).convert('L').resize((160,120),Image.Resampling.BOX),float)
Y,X=np.indices((120,160))
fx,fy,cx,cy=517.3/4,516.5/4,(318.6-1.5)/4,(255.3-1.5)/4
rays=np.array([(X-cx)/fx,(Y-cy)/fy,np.ones_like(X)]).reshape(3,-1)
zs=1/np.linspace(1/3,1/.45,80)
groups={k:[] for k in ['baseline',0,1,3]}
out=csv.writer(sys.stdout)
out.writerow(['reference','comparison','gap','retained','baseline_count','retained_pct','median_error_cm','mean_error_cm','within_10cm_pct'])
def report(i,j,k,e,n):
    metrics=[np.median(e)*100,e.mean()*100,100*np.mean(e<=.1)] if len(e) else [float('nan')]*3
    out.writerow([i,j,k,len(e),n,round(100*len(e)/n,3),*[round(x,4) for x in metrics]])
for i,j in [(20,25),(100,104),(180,184),(260,270),(340,344),(420,426),(500,504),(580,587),(660,666),(740,764)]:
    r,c=pose(i);s,kpos=pose(j);A,B=gray(i),gray(j);costs=[]
    for z in zs:
        q=s.T@(r@rays*z+(c-kpos)[:,None])
        u=(fx*q[0]/q[2]+cx).reshape(X.shape);v=(fy*q[1]/q[2]+cy).reshape(X.shape)
        b=map_coordinates(B,[v,u],order=1,mode='constant',cval=500.)
        costs.append(uniform_filter(abs(A-b),5))
    costs=np.array(costs);pred=zs[costs.argmin(0)]
    lo,hi=np.partition(costs,1,axis=0)[:2];gap=hi-lo
    di=np.argmin(abs(td-t[i]));assert abs(td[di]-t[i])<=.022
    gt=np.array(Image.open(depth[di]))[2::4,2::4]/5000
    m=(gt>=.45)&(gt<=3)&(X>5)&(X<154)&(Y>5)&(Y<114)&(lo<80)
    for k in groups:
        sel=m if k=='baseline' else m&(gap>k+1e-8)
        e=abs(pred[sel]-gt[sel]);groups[k].append(e)
        report(i,j,k,e,int(m.sum()))
n=sum(map(len,groups['baseline']))
for k,parts in groups.items(): report('pooled','all',k,np.concatenate(parts),n)
