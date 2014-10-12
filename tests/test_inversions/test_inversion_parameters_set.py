import unittest

import numpy as np
import scipy.sparse as sps

import viscojapan as vj
from viscojapan.inversion.inversion_parameters_set import InversionParametersSet


class TestInversionParametersSet(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_only_G_d(self):
        G = np.ones((10,50))
        d = np.ones((10,1))
        InversionParametersSet(G=G, d=d)

    def test_all_0(self):
        G = np.ones((10,5))
        d = np.ones((10,1))
        W = sps.eye(10)
        L = sps.csr_matrix((10,5))
        B = sps.csr_matrix((5,10))
        Bm0 = sps.csr_matrix((5,1))
        InversionParametersSet(G=G, d=d, W=W, B=B, L=L, Bm0=Bm0)
        
if __name__=='__main__':
    unittest.main()
