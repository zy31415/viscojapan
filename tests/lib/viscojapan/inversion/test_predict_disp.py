import unittest
from os.path import join

from viscojapan.inversion.predict_disp import DispPred
     
from viscojapan.test_utils import MyTestCase

class Test_results_file_reader(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test1(self):
        pred = DispPred(
            G_file = join(self.share_dir, 'G0_He50km_VisM6.3E18_Rake83.h5'),
            filter_sites_file = join(self.share_dir,'sites_0462'),
            result_file = join(self.share_dir,'nrough_06.h5'),
            )

        disp = pred.E_cumuslip(10)
        disp = pred.E_co()
        disp = pred.E_aslip(10)
        disp = pred.R_nth_epoch(3, 500)
        disp = pred.R_co(500)
        disp = pred.R_aslip(500)
        
        
        
        
if __name__ == '__main__':
    unittest.main()
