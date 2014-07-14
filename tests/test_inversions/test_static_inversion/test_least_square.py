import unittest
from os.path import join

from numpy import dot, ones, inf
import scipy.sparse as sparse
from viscojapan.least_square import LeastSquare
from viscojapan.epochal_data import EpochalG
from viscojapan.utils import get_this_script_dir
from viscojapan.inversion_test import gen_checkerboard_slip, gen_error_for_sites

this_test_path = get_this_script_dir(__file__)

class TestLeastSquare(unittest.TestCase):
    def setUp(self):
        G_file = '/home/zy/workspace/viscojapan/greens_function/050km-vis02/G.h5'
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
        lst = LeastSquare(
            G = self.G,
            d = self.d,
            L = sparse.eye(len(self.m_true))
            )
        
        lst.invert()
        lst.predict()
        lst.get_residual_norm()

    def test_LeastSquare_weighting(self):
        lst = LeastSquare(
            G = self.G,
            d = self.d,
            L = sparse.eye(len(self.m_true)),
            )        
        lst.invert()
        lst.predict()
        lst.get_residual_norm()


if __name__=='__main__':
    unittest.main()
