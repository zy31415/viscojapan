from os.path import join
import unittest

from pylab import plt

from viscojapan.plots.map_plot_fault import MapPlotFault
from viscojapan.epochal_data import EpochalIncrSlip
from viscojapan.fault_model import FaultFileIO
from viscojapan.utils import get_this_script_dir
from viscojapan.test_utils import MyTestCase


class Test_MapPlotFault(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        
        self.file_fault= join(self.share_dir,'fault.h5')
        self.file_incr_slip = join(self.share_dir, "incr_slip_a11_b00.h5")

    def test_pcolor_on_fault(self):
        ep = EpochalIncrSlip(self.file_incr_slip)
        fio = FaultFileIO(self.file_fault)

        slip = ep(0).reshape([fio.num_subflt_along_dip,
                              fio.num_subflt_along_strike])

        plot = MapPlotFault(self.file_fault)
        plot.pcolor_on_fault(slip)
        plt.savefig(join(self.outs_dir, 'pcolor_on_fault.png'))
        plt.close()
            
    def test_plot_slip(self):
        ep = EpochalIncrSlip(self.file_incr_slip)

        plot = MapPlotFault(self.file_fault)
        plot.plot_slip(ep(0))

        plt.savefig(join(self.outs_dir, 'plot_slip.png'))
        plt.close()
        
    def test_plot_fault(self):
        plot = MapPlotFault(self.file_fault)        
        plot.plot_fault()
        plt.savefig(join(self.outs_dir, 'plot_fault.png'))
        plt.close()
##
    def test_plot_slip_file(self):
        plot = MapPlotFault(self.file_fault)        
        plot.plot_slip_file(self.file_incr_slip, 0)
        plt.savefig(join(self.outs_dir, 'plot_slip_file.png'))
        plt.close()
        
    def test_plot_incr_slip_file(self):
        plot = MapPlotFault(self.file_fault)        
        plot.plot_incr_slip_file(self.file_incr_slip, 0)
        plt.savefig(join(self.outs_dir, 'plot_incr_slip_file.png'))
        plt.close()

    def test_plot_slip_contours(self):
        ep = EpochalIncrSlip(self.file_incr_slip)
        plot = MapPlotFault(self.file_fault)        
        plot.plot_slip_contours(ep(0),colors='k')
        plt.savefig(join(self.outs_dir, 'plot_slip_contours.png'))
        plt.close()
        

if __name__ =='__main__':
    unittest.main()
