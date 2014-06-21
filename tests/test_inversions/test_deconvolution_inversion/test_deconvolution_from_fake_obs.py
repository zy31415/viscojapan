from os.path import join
import unittest

from numpy.random import normal

from viscojapan.deconvolution_inversion import Deconvolution
from viscojapan.utils import get_this_script_dir, delete_if_exists

this_test_path = get_this_script_dir(__file__)

project_path = '/home/zy/workspace/viscojapan/'

class TestDeconvolution(unittest.TestCase):
    def setUp(self):
        self.file_results = join(this_test_path, 'res.h5')
        delete_if_exists(self.file_results)
        
        self.file_incr_slip = join(this_test_path, 'res_incr_slip.h5')
        delete_if_exists(self.file_incr_slip)

        self.file_slip = join(this_test_path, 'res_slip.h5')
        delete_if_exists(self.file_slip)

        self.file_pred_disp = join(this_test_path, 'res_pred_disp.h5')
        delete_if_exists(self.file_pred_disp)
        
    def test(self):
        dtest = Deconvolution()

        dtest.file_G = join(project_path, 'greensfunction/050km-vis02/G.h5')
        dtest.file_d = join(this_test_path, 'simulated_disp.h5')
        dtest.sites_filter_file = join(this_test_path, 'sites_0462')
        dtest.epochs = [0, 100, 1000]
        alpha = 1.
        beta = 1.

        dtest.load_data()
        dtest.invert(alpha, beta)
        dtest.predict()

        dtest.res_writer.save_results(self.file_results)
        dtest.res_writer.save_results_incr_slip(self.file_incr_slip)
        dtest.res_writer.save_results_pred_disp(self.file_pred_disp)
        dtest.res_writer.save_results_slip(self.file_slip)
        
if __name__=='__main__':
    unittest.main()
