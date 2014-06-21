#!/usr/bin/env python3
import sys

from numpy import logspace

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.occam_algorithm.occam_inversion import OccamInversion

from days import days as epochs
from alphas import alphas

inv = OccamInversion()

inv.sites_file = 'sites'
inv.file_G1 = '../greensfunction/050km-vis02/G.h5'
inv.file_G2 = '../greensfunction/050km-vis01/G.h5'
inv.f_d = 'cumu_post.h5'
inv.f_slip0 = 'slip0.h5'
inv.epochs = epochs
inv.init()

for ano, alpha in enumerate(alphas):
    inv.init_least_square()
    inv.invert(alpha)
    inv.pickle('outs/res_%02d.pkl'%ano)


