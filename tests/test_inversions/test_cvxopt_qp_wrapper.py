import unittest

import numpy as np
import scipy.sparse as sps

import viscojapan as vj
from viscojapan.inversion.cvxopt_qp_wrapper import CvxoptQpWrapper
from viscojapan.inversion.inversion_parameters_set import InversionParametersSet

class TestCvxoptQpWrapper(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_nonnegative(self):
        P = np.identity(10)
        q = np.ones((10,1))
        ls = CvxoptQpWrapper(P=P, q=q)
        ls.invert()
        print(ls.solution['x'])

    def test_negative(self):
        P = np.identity(10)
        q = np.ones((10,1))
        ls = CvxoptQpWrapper(P=P, q=q)
        ls.invert(False)
        print(ls.solution['x'])

    def test_create_from_inversion_parameters_set(self):
        G = np.ones((10,5))
        d = np.ones((10,1))
        ps = InversionParametersSet(G=G, d=d)

        ls = CvxoptQpWrapper.create_from_inversion_parameters_set(ps)
        ls.invert()
        print(ls.solution['x'])
        
        
        
if __name__=='__main__':
    unittest.main()
