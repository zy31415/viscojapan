import unittest
from os.path import join

from pylab import plt

import viscojapan as vj
from viscojapan.test_utils import MyTestCase
from viscojapan.utils import make_grids


class Test_make_grids(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)

    def test_make_grids(self):
        north = 80
        south = 12
        east = 200
        west = 80
        dx = 200e3
        dy = 200e3
        grids = make_grids(north, south, west, east, dx, dy)

        lons = [ii[0] for ii in grids]
        lats = [ii[1] for ii in grids]
        
        bm = vj.plots.MyBasemap(
            region_box = (west+20, south-40, east+70, north),
            x_interval = 20,
            y_interval = 20)
        bm.plot(lons, lats, 'x', latlon=True)
        plt.savefig(join(self.outs_dir, 'map_gridding_point.png'))


if __name__=='__main__':
    unittest.main()
    
