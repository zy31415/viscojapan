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
        reader = ResultFileReader(join(self.share_dir,'out.h5'))
        slip = reader.incr_slip
        num_subflts = reader.num_subflts

        slip = reader.get_incr_slip_at_nth_epoch(0)

        reader.num_sites

        reader.get_disp_at_nth_epoch(2)

        reader.get_disp_at_epoch(10)

        slip = reader.get_total_slip_at_nth_epoch(1)
        
        
        
        
if __name__ == '__main__':
    unittest.main()
