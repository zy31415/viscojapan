import unittest
from os.path import join

from numpy import dot, eye, ones, inf

from viscojapan.least_square import LeastSquare, LeastSquareTik2
from viscojapan.epochal_data import EpochalG
from viscojapan.utils import get_this_script_dir
from viscojapan.inversion_test import gen_checkerboard_slip, gen_error_for_sites

this_test_path = get_this_script_dir(__file__)

class TestLeastSquare(unittest.TestCase):
    def setUp(self):
        G_file = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
        sites_file = join(this_test_path, 'sites')

        ep_G = EpochalG(G_file, sites_file)

        G =  ep_G(0)
        slip = gen_checkerboard_slip(25, 10, 2, 2)*5.
        m = slip.reshape([-1, 1])
        d = dot(G,m)
        error = gen_error_for_sites(1300)
        d += error

        self.G = G
        self.d = d
        self.m_true = m

    def test_LeastSquare(self):
        lst = LeastSquare()
        lst.G = self.G
        lst.d = self.d
        lst.L = eye(len(self.m_true))

        lst.invert()
        lst.predict()
        lst.get_residual_norm()

    def test_LeastSquare_weighting(self):
        lst = LeastSquare()
        lst.G = self.G
        lst.d = self.d
        lst.L = eye(len(self.m_true))
        lst.sig = ones(len(lst.d))*0.1
        lst.sig[0] = inf
        
        lst.invert()
        lst.predict()
        lst.get_residual_norm()

    def test_LeastSquareTik2(self):
        lst = LeastSquareTik2()
        lst.G = self.G
        lst.d = self.d

        lst.invert(1., 2.)
        lst.predict()
        lst.get_residual_norm()
        lst.get_spatial_roughness()
        self.assertRaises(ValueError, lst.get_temporal_roughness)
        lst.num_epochs()
        

if __name__=='__main__':
    unittest.main()
