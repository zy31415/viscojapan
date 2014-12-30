import unittest
from os.path import join

import viscojapan as vj
     
from viscojapan.utils import get_this_script_dir
from viscojapan.test_utils import MyTestCase

class Test_disp_analyser(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test1(self):
        result_file = join(self.share_dir,'nrough_06_naslip_11.h5')        
        ana = vj.inv.DispAnalyser(result_file)
        ana.get_cumu_pred_3d()
        
if __name__ == '__main__':
    unittest.main()
