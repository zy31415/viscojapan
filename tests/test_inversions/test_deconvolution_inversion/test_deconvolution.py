from os.path import join
import unittest

from numpy.random import normal

from viscojapan.inversion import Deconvolution
from viscojapan.inversion.basis_function import BasisMatrix
from viscojapan.inversion.regularization import create_roughening_temporal_regularization
from viscojapan.utils import get_this_script_dir, delete_if_exists
from viscojapan.test_utils import MyTestCase


class TestDeconvolution(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

##    def test_DeconvolutionTestFromFakeObs(self):
##        dtest = DeconvolutionTestFromFakeObs()
##
##        dtest.file_G = join(project_path, 'greensfunction/050km-vis02/G.h5')
##        dtest.file_d = join(this_test_path, 'simulated_disp.h5')
##        dtest.sites_filter_file = join(this_test_path, 'sites_0462')
##        dtest.epochs = [0, 100, 1000]
##
##        dtest.num_err = 462*len(dtest.epochs)
##        dtest.east_st=6e-3
##        dtest.north_st=6e-3
##        dtest.up_st=20e-3
##
##        dtest.load_data()
##
##        lcurve = LCurve(dtest)
##        
##        lcurve.outs_dir = self.outs_dir
##        lcurve.alphas = [0,1]
##        lcurve.betas = [0,1]
##
##        lcurve.compute_L_curve()

    def test_Deconvoluation(self):

        file_G = join(self.share_dir, 'G.h5')
        file_d = join(self.share_dir, 'cumu_post_with_seafloor.h5')
        file_sd = join(self.share_dir, 'sites_sd.h5')
        file_sites_filter = join(self.share_dir, 'sites_0462')
        fault_file = join(self.share_dir, 'fault_He50km_east.h5')

        epochs = [0, 10, 30]

        basis = BasisMatrix.create_from_fault_file(fault_file, len(epochs))
        rough = 1.
        temp = 1.
        reg = create_roughening_temporal_regularization(
            fault_file, epochs, rough, temp)

        inv = Deconvolution(
            file_G = file_G,
            file_d = file_d,
            file_sd = file_sd,
            file_sites_filter = file_sites_filter,
            epochs = epochs,
            regularization = reg,
            basis = basis
            )

        inv.set_data_all()
        inv.invert()

        
if __name__=='__main__':
    unittest.main()
