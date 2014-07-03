from os.path import join
import unittest

from pylab import plt

from viscojapan.plots.my_basemap import MyBasemap
from viscojapan.plots.map_plot_slab import MapPlotSlab
from viscojapan.plots.map_plot_fault import MapPlotFault

from viscojapan.utils import get_this_script_dir
this_script_dir = get_this_script_dir(__file__)

class Test_MyBasemap(unittest.TestCase):
    def setUp(self):
        pass

    def test_initialization(self):
        bm = MyBasemap()
        self.assertRaises(AssertionError, MyBasemap, xxx='near')
        bm = MyBasemap(region_code='near')

    def test_share_basemap(self):
        bm = MyBasemap(x_interval = 1)

        p1 = MapPlotSlab(basemap = bm)
        p1.plot_top()
        
        p2 = MapPlotFault(fault_file=join(this_script_dir, 'share/fault.h5'),
                          basemap = bm)
        p2.plot_fault()

        plt.savefig(join(this_script_dir, '~plots/share_basemap.png'))
        plt.close()
        
        
if __name__ =='__main__':
    unittest.main()
