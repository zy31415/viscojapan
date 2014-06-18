#!/usr/bin/env python3
import sys

import h5py
from pylab import *


sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.plot_utils import plot_L

with h5py.File('../L-curve.h5','r') as fid:
    roughness = fid['roughness'][...]
    solution_norms = fid['solution_norms'][...]

alphas = logspace(-5,3,30)
plot_L(solution_norms, roughness, alphas)
legend()
show()
