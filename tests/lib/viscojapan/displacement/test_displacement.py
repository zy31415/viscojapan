import unittest
from os.path import join

import numpy as np

import viscojapan as vj


__author__ = 'zy'

class TestDisp(vj.test_utils.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_Disp(self):
        res_file = join(self.share_dir,'nrough_05_naslip_11.h5')
        reader = vj.inv.ResultFileReader(res_file)
        disp = reader.get_pred_disp()

        disp.cumu_disp3d
        disp.post_disp3d

        np.testing.assert_array_almost_equal(disp.get_co_disp(),
                                             disp.get_cumu_disp_at_nth_epoch(0))

        vel = disp.vel3d
        vel = disp.get_vel3d(unit='mm/yr')
        #print(vel)



if __name__ == '__main__':
    unittest.main()
