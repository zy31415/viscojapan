import os

import numpy  as np

import pGMT

import viscojapan as vj

res_file = '../../outs/nrough_05_naslip_11.h5'

plt = vj.inv.MisfitPlotter(res_file)
plt.plot('misfits.pdf')

    
