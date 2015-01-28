import unittest

from os.path import join
import viscojapan as vj

__author__ = 'zy'


class TestMomentCalculator(vj.test_utils.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_MomentCalculator(self):
        res_file = join(self.share_dir,'nrough_05_naslip_11.h5')
        fault_file = join(self.share_dir, 'fault_bott80km.h5')
        reader = vj.inv.ResultFileReader(res_file)
        slip = reader.get_slip(fault_file)

        earth_file = join(self.share_dir,'earth.model_He50km_VisM6.3E18')

        cal = vj.moment.MomentCalculator(fault_file, earth_file)

        mos, mws = cal.get_afterslip_Mos_Mws(slip)
        print(mos, mws)


if __name__ == '__main__':
    unittest.main()
