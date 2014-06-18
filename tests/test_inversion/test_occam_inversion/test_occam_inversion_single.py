from os.path import join
import os
import unittest

from viscojapan.occam_inversion import OccamInversionTik2
from viscojapan.utils import delete_if_exists, get_this_script_dir

from days import days as epochs

project_path = '/home/zy/workspace/viscojapan/'
this_test_path = get_this_script_dir(__file__)

class TestOccamInversionTik2(unittest.TestCase):
    def setUp(self):
        self.results_file = join(this_test_path,'res.h5')
        delete_if_exists(self.results_file )

        self.file_slip_results = join(this_test_path, 'res_incr_slip.h5')
        delete_if_exists(self.file_slip_results)

        self.file_pred_disp = join(this_test_path, 'res_pred_disp.h5')
        delete_if_exists(self.file_pred_disp)

    def test_occam_inversion(self):
        inv = OccamInversionTik2()
        inv.sites_file = join(this_test_path,'sites_0093')
        inv.file_G1 = join(project_path,'greensfunction/050km-vis02/G.h5')
        inv.file_G2 = join(project_path,'greensfunction/050km-vis01/G.h5')
        inv.f_d = join(project_path,'tsana/post_fit/cumu_post.h5')
        inv.f_slip0 = join(this_test_path,'slip0.h5')
        inv.epochs = epochs

        inv.nlin_par_initial_values = [18.890041118437537]
        inv.nlin_par_names = ['log10_visM']        

        inv.init()
        inv.load_data()
        
        alpha = 100
        inv.invert(alpha)
        inv.res_writer.save_results(self.results_file)
        inv.res_writer.save_results_incr_slip(self.file_slip_results)
        inv.res_writer.save_results_pred_disp(self.file_pred_disp)
        

if __name__ == '__main__':
    unittest.main()


    
