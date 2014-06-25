from os.path import join

import unittest

from numpy import logspace

from viscojapan.inversion_test.checkerboard_test_for_static_inversion import CheckerboardTest
from viscojapan.utils import get_this_script_dir

f_G = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
filter_site_file = 'sites'
filter_site_seafloor_file = 'sites_with_seafloor'

this_test_path = get_this_script_dir(__file__)


class TestCheckerboardTestForStaticInversion(unittest.TestCase):
    def setUp(self):
        self.alphas = logspace(-4,0,2)

    def test_inversion(self):
        test1 = CheckerboardTest()
        test1.f_G = f_G
        test1.filter_site_file = join(this_test_path, filter_site_file)
        test1.make_L_curve(self.alphas, join(this_test_path,'~plots'))

    def test_with_seafloor(self):
        test2 = CheckerboardTest()
        test2.f_G = f_G
        test2.filter_site_file = join(this_test_path, filter_site_seafloor_file)
        test2.make_L_curve(self.alphas, join(this_test_path, '~plots_with_seafloor'))
        

if __name__ =='__main__':
    unittest.main()
    
