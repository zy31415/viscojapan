from os.path import join
import unittest

from pylab import show, savefig, close

from viscojapan.plots.plot_utils import Map
from viscojapan.epochal_data import EpochalDisplacement, EpochalIncrSlip
from viscojapan.utils import get_this_script_dir

this_test_path = get_this_script_dir(__file__)

class TestPlots(unittest.TestCase):
    def setUp(self):
        self.file_disp = join(this_test_path,'pred_disp_a11_b00.h5')
        self.file_incr_slip = join(this_test_path,'incr_slip_a11_b00.h5')
        self.file_sites = join(this_test_path,'sites_with_seafloor')

    def test_plot_disp(self):
        ep = EpochalDisplacement(self.file_disp, self.file_sites)
        plot = Map()
        plot.plot_disp(ep(0), ep.filter_sites)
        savefig(join(this_test_path, '~plot_disp.png'))
        close()

    def test_plot_fault(self):
        plot = Map()
        plot.plot_fault(fno = 10)
        savefig(join(this_test_path, '~plot_fault.png'))
        close()

    def test_plot_fslip(self):
        ep = EpochalIncrSlip(self.file_incr_slip)
        plot = Map()
        plot.plot_fslip(ep(0))
        savefig(join(this_test_path, '~plot_incr_slip.png'))
        close()

    def test_plot_disp_file(self):
        plot = Map()
        plot.plot_disp_file(self.file_disp, 0)
        savefig(join(this_test_path, '~plot_disp_file.png'))
        close()

    def test_plot_slip_file(self):
        plot = Map()
        plot.plot_slip_file(self.file_incr_slip, 0)
        savefig(join(this_test_path, '~plot_slip_file.png'))
        close()

    def test_plot_incr_slip_file(self):
        plot = Map()
        plot.plot_incr_slip_file(self.file_incr_slip, 0)
        savefig(join(this_test_path, '~plot_incr_slip_file.png'))
        close()
        
        
if __name__ =='__main__':
    unittest.main()
