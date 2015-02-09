import unittest
from os.path import join

from pylab import plt

import viscojapan as vj

__author__ = 'zy'


class Test_plot_slip_and_rate_at_subflt(vj.test_utils.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_plot(self):
        res_file = join(self.share_dir,'nrough_05_naslip_11.h5')
        fault_file = join(self.share_dir, 'fault_bott80km.h5')
        reader = vj.inv.ResultFileReader(res_file)
        slip = reader.get_slip(fault_file)

        plotter = vj.slip.plot.plot_slip_and_rate_at_subflt(
            slip, 8, 8)

        plt.savefig(join(self.outs_dir, 'slip_and_rate.pdf'))

if __name__ == '__main__':
    unittest.main()
