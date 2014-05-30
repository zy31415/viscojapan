#!/usr/bin/env python3
''' For a non-linear inverison to run, you need this information:
(1) dG versus non-linear parameters
(2) G
(3) slip  - initial value
(4) obs 
'''

import sys

sys.path.append('/home/zy/workspace/greens/lib')
from greens.formulate_occam import FormulatOccam
from greens.jacobian_vec import JacobianVec
from greens.ed_sites_filtered import EDSitesFiltered
from greens.diff_ed import DiffED
from greens.epochal_data import EpochalData
from days import days

file_G1 = '../greensfunction/050km-vis00/G.h5'
file_G2 = '../greensfunction/050km-vis01/G.h5'
sites_file = 'sites_test'

f_m0 = 'model.h5'
m0 = EpochalData(f_m0)

f_d = 'obs.h5'
obs = EDSitesFiltered(f_d, sites_file)


G1 = EDSitesFiltered(file_G1, sites_file)
G2 = EDSitesFiltered(file_G2, sites_file)

dG = DiffED(G1, G2, 'log10_visM')

jac = JacobianVec(dG, m0)

form = FormulatOccam()
form.epochs = days
form.non_lin_par_vals = [5.83983824100718e+18]
form.non_lin_JacobianVecs = [jac]
form.G = G1
form.d = obs

d=form.d_()
print(d.shape)
Jac = form.Jacobian()
print(Jac.shape)

