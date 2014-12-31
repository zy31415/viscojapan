import os

import numpy  as np

import pGMT

import viscojapan as vj

nrough = 6
naslip =11
res_file = '../../outs/nrough_%02d_naslip_%02d.h5'%(nrough, naslip)

plt = vj.inv.MisfitPlotter(res_file)
plt.plot()
plt.combine('misfits_nrough_%02d_naslip_%02d.pdf'%(nrough, naslip))

def rms(arr):
    return np.sqrt(np.mean(arr**2))

for key, value in plt.rms.items():
    print(key, rms(value))
    
