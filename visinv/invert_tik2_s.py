#!/usr/bin/env python3
import sys

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.occam_algorithm.occam_inversion import OccamInversion
from days import days as epochs

inv = OccamInversion()

inv.sites_file = 'sites'
inv.file_G1 = '../greensfunction/050km-vis02/G.h5'
inv.file_G2 = '../greensfunction/050km-vis01/G.h5'
inv.f_d = 'cumu_post.h5'
inv.f_slip0 = 'slip0.h5'
inv.epochs = epochs
inv.init()
inv.init_least_square()

alpha = 100
inv.invert(alpha)
#inv.pickle('test.pkl')
inv.save_raw_results('raw_res.h5')
inv.save_results_to_epochal_file('epochal_res.h5')
