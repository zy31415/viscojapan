from os.path import join
import unittest

from pylab import show, savefig, close

from viscojapan.plots.map_plot_fault import MapPlotFault
from viscojapan.epochal_data import EpochalIncrSlip

from viscojapan.utils import get_this_script_dir

this_test_path = get_this_script_dir(__file__)

class Test_MapPlotFault(unittest.TestCase):
    def setUp(self):
        self.file_fault= join(this_test_path,'fault.h5')
        self.file_incr_slip = join(this_test_path, "incr_slip_a11_b00.h5")

    def test_plot_fault(self):
        plot = MapPlotFault(self.file_fault)        
        plot.plot_fault()
        savefig(join(this_test_path, '~plot_fault.png'))
        close()

    def test_plot_slip(self):
        ep = EpochalIncrSlip(self.file_incr_slip)
        plot = MapPlotFault(self.file_fault)        
        plot.plot_slip(ep(0))
        savefig(join(this_test_path, '~plot_slip.png'))
        close()

    def test_plot_slip_file(self):
        plot = MapPlotFault(self.file_fault)        
        plot.plot_slip_file(self.file_incr_slip, 0)
        savefig(join(this_test_path, '~plot_slip_file.png'))
        close()
        
    def test_plot_incr_slip_file(self):
        plot = MapPlotFault(self.file_fault)        
        plot.plot_incr_slip_file(self.file_incr_slip, 0)
        savefig(join(this_test_path, '~plot_incr_slip_file.png'))
        close()

    def test_plot_slip_contours(self):
        ep = EpochalIncrSlip(self.file_incr_slip)
        plot = MapPlotFault(self.file_fault)        
        plot.plot_slip_contours(ep(0),colors='k')
        savefig(join(this_test_path, '~plot_slip_contours.png'))
        close()
        

if __name__ =='__main__':
    unittest.main()
