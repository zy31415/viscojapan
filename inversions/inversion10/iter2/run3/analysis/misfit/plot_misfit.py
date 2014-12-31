import os

import numpy  as np

import pGMT

import viscojapan as vj

res_file = '../../outs/nrough_06_naslip_11.h5'

plt = vj.inv.MisfitPlotter(res_file)
plt.plot('misfits.pdf')
#plt.combine('misfits.pdf')

##def rms(arr):
##    return np.sqrt(np.mean(arr**2))
##
##for key, value in plt.rms.items():
##    print(key, rms(value))
    
