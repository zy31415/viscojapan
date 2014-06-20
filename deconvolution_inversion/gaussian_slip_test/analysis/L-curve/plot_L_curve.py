#!/usr/bin/env python3
import h5py
from pylab import *

from viscojapan.plot_utils import plot_L

from alphas import alphas

nroughs =[]
nsol = []
for ano, alpha in enumerate(alphas):
    print(ano)
    with h5py.File('../../outs0/res_%02d.h5'%ano,'r') as fid:
        roughness = fid['roughness'][...]
        solution_norms = fid['residual_norm'][...]
        nroughs.append(roughness)
        nsol.append(solution_norms)

alphas = logspace(-5,3,30)
plot_L(nsol, nroughs, alphas)
legend()
show()
