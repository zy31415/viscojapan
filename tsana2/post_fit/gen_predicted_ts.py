#!/usr/bin/env python3
''' This script generates predicated cumulative postseismic displacement.
.
-ZY, 4/11/14
'''
import os
from os.path import *
from pylab import *
import pickle
from h5py import File

_dir_cfs_post='CFS_POST'


def get_trange(site):
    with File('../timeseries/igs08.h5','r') as fid:
        t=fid[site+'/t'][...]
    return amin(t),amax(t)
        


fpred=File('ts_pred.h5','w')
fpred['info/readme']='''This file records predicated time series.
The time series in this file can be used to compare with observation.
'''

for f in os.listdir(_dir_cfs_post):
    with open(join(_dir_cfs_post,f),'rb') as fid:
        cfs=pickle.load(fid)
    site=f[0:4]
    print(site)
    t1,t2=get_trange(site)
    ts=range(t1,t2+1)
    fpred[site+'/t']=ts
    for cf in cfs:
        ys=cf.func(ts)
        fpred[site+'/'+cf.CMPT]=ys
fpred.close()

