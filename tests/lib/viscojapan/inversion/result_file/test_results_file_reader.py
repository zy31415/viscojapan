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
            join(self.share_dir,'nrough_06_naslip_11.h5')
            )
        
        slip = reader.incr_slip
        reader.num_sites        
        
if __name__ == '__main__':
    unittest.main()
