import unittest
from os.path import join

import h5py

from viscojapan.test_utils import MyTestCase
from viscojapan.earth_model.mo import ComputeMoment

class Test_ComputeMoment(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_ComputeMoment(self):
        fault_file = join(self.share_dir, 'fault_bott60km.h5')
        earth_file = join(self.share_dir, 'earth.model_He50')
        com = ComputeMoment(fault_file, earth_file)
        res_file = join(self.share_dir, 'ano_10.h5')
        with h5py.File(res_file) as fid:
            Bm = fid['Bm'][...]
            slip = Bm[0:-1]
        mo, mw = com.moment(slip)
        print(mo, mw)
    


if __name__=='__main__':
    unittest.main()
