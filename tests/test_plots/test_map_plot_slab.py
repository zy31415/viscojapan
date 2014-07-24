from os.path import join
import unittest

from pylab import plt

from viscojapan.plots.map_plot_slab import MapPlotSlab
from viscojapan.plots.map_plot_fault import MapPlotFault

from viscojapan.utils import get_this_script_dir

this_test_path = get_this_script_dir(__file__)

class Test_MapPlotSlab(unittest.TestCase):
    def setUp(self):
        pass

    def test_plot_fault(self):
        plot = MapPlotSlab()        
        plot.plot_top()
        
        plt.savefig(join(this_test_path, '~outs/plot_slab_top.png'))
        plt.close()

    def test_plot_dep_contour(self):
        plot = MapPlotSlab()
        plot.plot_dep_contour(-20, color='red')
        plot.plot_dep_contour(-40, color='blue')
        plot.plot_dep_contour(-60, color='black')
        plt.savefig(join(this_test_path, '~outs/plot_dep_contour.png'))
        plt.close()

if __name__ =='__main__':
    unittest.main()
