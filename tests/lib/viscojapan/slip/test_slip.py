import unittest

from os.path import join
import viscojapan as vj

__author__ = 'zy'


class TestSlip(vj.test_utils.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_Slip(self):
        res_file = join(self.share_dir,'nrough_05_naslip_11.h5')
        fault_file = join(self.share_dir, 'fault_bott80km.h5')
        reader = vj.inv.ResultFileReader(res_file)
        slip = reader.get_slip(fault_file)

        s_afterslip = slip.afterslip3d
        s_co = slip.get_coseismic_slip()
        s_3d_incr_slip = slip.incr_slip3d
        rate = slip.get_slip_rate_at_nth_epoch(1)

if __name__ == '__main__':
    unittest.main()
