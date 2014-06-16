#!/usr/bin/env python3
import sys
from os.path import join
import os

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.occam_algorithm.occam_inversion import OccamInversion
from days import days as epochs

project_path = '/home/zy/workspace/viscojapan/'
this_test_path = os.path.dirname(os.path.realpath(__file__))

inv = OccamInversion()

inv.sites_file = join(this_test_path,'sites_0093')
inv.file_G1 = join(project_path,'greensfunction/050km-vis02/G.h5')
inv.file_G2 = join(project_path,'greensfunction/050km-vis01/G.h5')
inv.f_d = join(project_path,'tsana/post_fit/cumu_post.h5')
inv.f_slip0 = join(this_test_path,'slip0.h5')
inv.epochs = epochs
inv.init()
inv.init_least_square()

alpha = 100
inv.invert(alpha)
#inv.pickle('test.pkl')
inv.save_raw_results('raw_res.h5')
inv.save_results_to_epochal_file('epochal_res.h5')
