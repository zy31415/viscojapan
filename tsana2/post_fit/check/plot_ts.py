#!/usr/bin/env python3
from pylab import *
from h5py import File

site=b'J550-u'
ts=range(0,1200)
ys=[]
with File('../cumupost_pred.h5') as fid:
    rows=fid['rows'][...]
    idx=where(rows==site)
    for ti in ts:
        ys.append(fid['%04d'%ti][...][idx][0])


plot(ts,ys)
show()
