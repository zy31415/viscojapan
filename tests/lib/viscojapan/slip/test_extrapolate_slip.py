import unittest
from os.path import join

import viscojapan as vj

__author__ = 'zy'


class Test_SlipExtrapolation(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_SlipExtrapolationLOG(self):
        res_file = '/home/zy/workspace/viscojapan/tests/share/nrough_05_naslip_11.h5'
        reader = vj.inv.ResultFileReader(res_file)
        slip = reader.get_slip()

        output_file = join(self.outs_dir, 'extra_slip_LOG.h5')

        epochs = list(range(0,1621, 60)) + list(range(365*5, 365*27+1, 365))

        gen = vj.slip.SlipExtrapolationLOG(
            slip = slip,
            epochs = epochs,
            output_file = output_file,
        )

        gen.go()

    def test_SlipExtrapolationEXP(self):
        res_file = '/home/zy/workspace/viscojapan/tests/share/nrough_05_naslip_11.h5'
        reader = vj.inv.ResultFileReader(res_file)
        slip = reader.get_slip()

        output_file = join(self.outs_dir, 'extra_slip_EXP.h5')

        epochs = list(range(0,1621, 60)) + list(range(365*5, 365*27+1, 365))

        gen = vj.slip.SlipExtrapolationEXP(
            slip = slip,
            epochs = epochs,
            output_file = output_file,
        )

        gen.go()




if __name__ == '__main__':
    unittest.main()
