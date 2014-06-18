from os.path import join
import unittest

from numpy.random import normal

from viscojapan.deconvolution_inversion import DeconvolutionTestFromFakeObs
from viscojapan.utils import get_this_script_dir, delete_if_exists

this_test_path = get_this_script_dir(__file__)

project_path = '/home/zy/workspace/viscojapan/'

class TestDeconvolutionTestFromFakeObs(unittest.TestCase):
    def setUp(self):
        self.file_results = join(this_test_path, 'res.h5')
        delete_if_exists(self.file_results)
        
        self.file_slip_results = join(this_test_path, 'res_slip.h5')
        delete_if_exists(self.file_slip_results)

        self.file_pred_disp = join(this_test_path, 'res_pred_disp.h5')
        delete_if_exists(self.file_pred_disp)
        

    def test(self):
        dtest = DeconvolutionTestFromFakeObs()

        dtest.file_G = join(project_path, 'greensfunction/050km-vis02/G.h5')
        dtest.file_fake_d = join(project_path, 'deconvolution_inversion/simulated_disp.h5')
        dtest.sites_filter_file = join(this_test_path, 'sites_0462')
        dtest.epochs = [0, 100, 1100]

        dtest.init()
        dtest.load_data()
        alpha = 1.
        dtest.invert(alpha)
        dtest.save_results(self.file_results)
        dtest.save_results_slip(self.file_slip_results)
        dtest.save_results_pred_disp(self.file_pred_disp)
        
if __name__=='__main__':
    unittest.main()
