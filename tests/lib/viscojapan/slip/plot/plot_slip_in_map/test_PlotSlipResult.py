import unittest

from os.path import join
import viscojapan as vj

__author__ = 'zy'


class Test_PlotSlipResult(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_Slip(self):
        output_file = join(self.outs_dir, 'slip.pdf',)

        plt = vj.slip.plot.PlotSlipResult(
            fault_file = '/home/zy/workspace/viscojapan/tests/share/fault_bott80km.h5',
            result_file = '/home/zy/workspace/viscojapan/tests/share/nrough_05_naslip_11.h5',
            subplot_width = 3.2,
            subplot_height = 5.2,
            num_plots_per_row = 5,
            earth_file = '/home/zy/workspace/viscojapan/tests/share/earth.model_He50km_VisM6.3E18',
            color_label_interval_aslip = .3,
            )

        plt.plot()
        plt.save(output_file)

if __name__ == '__main__':
    unittest.main()
