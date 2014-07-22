import h5py
import unittest
from os.path import join

from viscojapan.test_utils import MyTestCase
from viscojapan.epochal_data import break_col_vec_into_epoch_file

class Test_Slip_IncrSlip_conversion(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test(self):
        fid = h5py.File(join(self.share_dir, 'ano_10_bno_10.h5'))
        m = fid['m'][...]
        epochs = [0, 1, 2, 5, 10, 15, 21, 28, 37, 47, 57, 70,
                  87, 106, 132, 166, 211, 275, 367, 523, 1100]
        
        break_col_vec_into_epoch_file(m, epochs,
                                      join(self.outs_dir, 'incr_slip.h5'))


if __name__ == '__main__':
    unittest.main()
