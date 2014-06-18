import sys
import unittest

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.occam_algorithm.occam_inversion import OccamInversion
from days import days as epochs

class TestOccamInversion(unittest.TestCase):
    def setUp(self):
        pass

    def test(self):
        inv = OccamInversion()
        inv.sites_file = 'sites'
        inv.file_G1 = '../greensfunction/050km-vis02/G.h5'
        inv.file_G2 = '../greensfunction/050km-vis01/G.h5'
        inv.f_d = 'cumu_post.h5'
        inv.f_slip0 = 'slip0.h5'
        inv.epochs = epochs
        alpha = 100
        inv.init()
        inv.init_least_square()
        inv.invert(alpha)
        inv.pickle('test.pkl')

if __name__=='__main__':
    unittest.main()

