import unittest
from os.path import join

from viscojapan.gaussian_slip import GaussianSlip
from viscojapan.deconvolution_inversion import ForwardConvolution
from viscojapan.utils import get_this_script_dir, delete_if_exists

this_test_path = get_this_script_dir(__file__)

class TestForwardConvolution(unittest.TestCase):
    def setUp(self):
        # simulated slip on the fault
        gaussian_slip = GaussianSlip()
        gaussian_slip.num_subflts_in_dip = 10
        gaussian_slip.num_subflts_in_strike = 25

        gaussian_slip.mu_dip = 4.
        gaussian_slip.mu_stk = 12.
        gaussian_slip.sig_dip = 2
        gaussian_slip.sig_stk = 5

        # temporal part
        gaussian_slip.max_slip0 = 10.
        gaussian_slip.log_mag = 1.
        gaussian_slip.tau = 5.
        
        com = ForwardConvolution()
        com.file_G = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
        com.slip = gaussian_slip
        com.file_output = join(this_test_path,'simulated_disp.h5')

        delete_if_exists(com.file_output)

        self.com_disp = com

    def test_add_epochs(self):
        com_disp  = self.com_disp        
        com_disp.init()
        com_disp.init_output_file()
        com_disp.add_epochs(range(0,10))

    def test_mp_add_epochs(self):
        com_disp  = self.com_disp        
        com_disp.init()
        com_disp.init_output_file()
        com_disp.mp_add_epochs(range(0,20),3)
        
    
