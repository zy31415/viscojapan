#!/usr/bin/env python3
''' For a non-linear inverison to run, you need this information:
(1) dG versus non-linear parameters
(2) G
(3) slip  - initial value
(4) obs 
'''

import sys

from numpy import log10

sys.path.append('/home/zy/workspace/greens/lib')
from greens.formulate_occam import FormulatOccamPostseismic
from greens.jacobian_vec import JacobianVec
from greens.ed_sites_filtered import EDSitesFiltered
from greens.diff_ed import DiffED
from greens.epochal_data import EpochalData
from greens.invert import Invert
from days import days

sites_file = 'sites'

file_G1 = '../greensfunction/050km-vis00/G.h5'
G1 = EDSitesFiltered(file_G1, sites_file)

file_G2 = '../greensfunction/050km-vis01/G.h5'
G2 = EDSitesFiltered(file_G2, sites_file)

dG = DiffED(G1, G2, 'log10_visM')

f_m0 = 'model.h5'
m0 = EpochalData(f_m0)

f_d = 'post.h5'
obs = EDSitesFiltered(f_d, sites_file)

visM = 5.83983824100718e+18
log10_visM = log10(visM)

jac_1 = JacobianVec(dG, m0)

form = FormulatOccamPostseismic()
form.epochs = days
form.non_lin_par_vals = [log10_visM]
form.non_lin_JacobianVecs = [jac_1]
form.G = G1
form.d = obs

d_=form.d_()
print(d_.shape)
jacobian = form.Jacobian()
print(jacobian.shape)

inv = Invert()
inv.G = jacobian
inv.d = d_
inv.alpha = 100.

inv()

