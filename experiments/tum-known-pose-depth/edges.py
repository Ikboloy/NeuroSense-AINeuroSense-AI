"""Usage: python edges.py PATH_TO_EXTRACTED_freiburg1_xyz > edges.csv"""
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
groups={}
out=csv.writer(sys.stdout)
out.writerow("pair region gap eligible retained retention_pct median_error_cm mean_error_cm".split())
def report(pair,region,k,n,e):
    out.writerow([pair,region,k,n,len(e),round(100*len(e)/n,2) if n else "",round(100*np.median(e),2) if len(e) else "",round(100*np.mean(e),2) if len(e) else ""])
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
    valid=(gt>=.45)&(gt<=3)
    near=m&(gt<=1)
    edge=np.zeros_like(m); interior=near.copy()
    for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
        adj=np.roll(gt,(dy,dx),(0,1))
        ok=np.roll(valid,(dy,dx),(0,1))
        edge |= near&ok&(adj-gt>=.15)
        interior &= ok&(abs(adj-gt)<.15)
    for name,region in [('all',m),('near_edge',edge),('near_interior',interior)]:
        for k in ['baseline',0,1,3]:
            mask=region if k=='baseline' else region&(gap>k+1e-8)
            e=abs(pred[mask]-gt[mask]); n=int(region.sum())
            groups.setdefault((name,k),[]).append((n,e))
            report(f'{i}:{j}',name,k,n,e)
for (name,k),parts in groups.items():
    report('pooled',name,k,sum(n for n,_ in parts),np.concatenate([e for _,e in parts]))
