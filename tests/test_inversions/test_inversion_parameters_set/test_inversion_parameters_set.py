import unittest

import numpy as np

import viscojapan as vj
from viscojapan.inversion.inversion_parameters_set import InversionParametersSet


class TestInversionParametersSet(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test1(self):
        G = np.ones((10,5))
        d = np.ones((10,1))
        InversionParametersSet(G=G, d=d)
        
if __name__=='__main__':
    unittest.main()
