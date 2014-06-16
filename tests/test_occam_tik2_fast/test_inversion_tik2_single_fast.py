#!/usr/bin/env python3
import sys
from os.path import join
import os
import unittest

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.occam_algorithm.occam_inversion import OccamInversion
from viscojapan.utils import delete_if_exists, get_this_script_dir

from days import days as epochs

project_path = '/home/zy/workspace/viscojapan/'
this_test_path = get_this_script_dir(__file__)

class TestOccamInversionTik2FAST(unittest.TestCase):
    def setUp(self):
        self.file_raw_results = join(this_test_path,'raw_res.h5')
        self.file_epochal_file_resutls = join(this_test_path,
                                              'epochal_results.h5')

        delete_if_exists(self.file_raw_results)
        delete_if_exists(self.file_epochal_file_resutls)        

    def test(self):
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
        inv.save_raw_results(self.file_raw_results)
        inv.save_results_to_epochal_file(self.file_epochal_file_resutls)

if __name__ == '__main__':
    unittest.main()


    
