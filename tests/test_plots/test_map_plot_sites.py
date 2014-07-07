from os.path import join
import unittest

from pylab import show, savefig, close

from viscojapan.plots.my_basemap import MyBasemap
from viscojapan.plots.map_plot_sites import MapPlotDisplacement

from viscojapan.epochal_data import EpochalDisplacement

from viscojapan.test_utils import MyTestCase

class TestMapPlotDisplacement(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        
        self.file_disp = join(self.share_dir, 'pred_disp_a11_b00.h5')

    def test_MyBasemap(self):
        mybm = MyBasemap()

    def test_plot_disp(self):
        ep = EpochalDisplacement(self.file_disp)
        plot = MapPlotDisplacement()
        plot.plot_disp(ep(0), ep.filter_sites)
        savefig(join(self.outs_dir, 'plot_disp.png'))
        close()

    def test_plot_disp_file(self):
        plot = MapPlotDisplacement()
        plot.plot_disp_file(self.file_disp, 0)
        savefig(join(self.outs_dir, 'plot_disp_file.png'))
        close()
        

        
if __name__ =='__main__':
    unittest.main()
