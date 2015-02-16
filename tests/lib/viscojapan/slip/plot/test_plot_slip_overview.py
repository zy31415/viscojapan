import unittest
from os.path import join

import viscojapan as vj

__author__ = 'zy'


class Test_slip_overviewer(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_plot(self):
        res_file = '/home/zy/workspace/viscojapan/tests/share/nrough_05_naslip_11.h5'
        reader = vj.inv.ResultFileReader(res_file)
        slip = reader.get_slip()

        plotter = vj.slip.plot.plot_slip_overview(
            slip,
            join(self.outs_dir, 'slip_history.pdf')
            )

if __name__ == '__main__':
    unittest.main()
