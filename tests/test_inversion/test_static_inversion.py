import unittest
from os.path import join

from viscojapan.static_inversion import CheckerboardTestForStaticInversion
from viscojapan.utils import get_this_script_dir

this_test_path = get_this_script_dir(__file__)

class TestCheckerboardTestForStaticInversion(unittest.TestCase):
    def setUp(self):
        pass
    def test(self):
        chb = CheckerboardTestForStaticInversion()
        chb.f_G = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
        chb.filter_site_file = join(this_test_path, 'sites')
        alpha = 100

        chb.load_data()
        chb.invert(100)

if __name__ == '__main__':
    unittest.main()
