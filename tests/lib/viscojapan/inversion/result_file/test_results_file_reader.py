import unittest
from os.path import join

from viscojapan.inversion.result_file import \
     ResultFileReader
     
from viscojapan.utils import get_this_script_dir
from viscojapan.test_utils import MyTestCase

class Test_results_file_reader(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test1(self):
        reader = ResultFileReader(
            '/home/zy/workspace/viscojapan/tests/share/nrough_05_naslip_11.h5'
            )
        
        slip = reader.incr_slip
        reader.num_sites
        reader.get_obs_disp()
        reader.get_pred_disp()
        print(reader.get_slip())
        
if __name__ == '__main__':
    unittest.main()
