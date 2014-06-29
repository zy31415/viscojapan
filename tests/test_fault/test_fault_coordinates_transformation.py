import unittest
from os.path import join
import warnings

from numpy import arange, meshgrid, ascontiguousarray, linspace
from numpy.testing import assert_almost_equal
from pylab import plt

from viscojapan.fault.transform import FaultCoordinatesTransformation
from viscojapan.utils import get_this_script_dir
from viscojapan.plots.plot_utils import Map

this_test_path = get_this_script_dir(__file__)

class TestFaultCoordinatesTransformation(unittest.TestCase):
    def setUp(self):
        self.fm = FaultCoordinatesTransformation()

        self.plt_map = Map()
        self.plt_map.init()

    def test__lonlat_to_xy(self):
        B0 = self.fm.B0
        x, y = self.fm._lonlat_to_xy(B0[0], B0[1])
        self.assertEqual(x,0)
        self.assertEqual(y,0)

    def test_ground2geo(self):
        xg = linspace(0.001, 425, 25)
        yg = linspace(0, 700, 30)
        xxg, yyg = meshgrid(xg, yg)
        
        LLons, LLats = self.fm.ground2geo(xxg, yyg)

        self.plt_map.plot(LLons,LLats,color='gray',latlon=True)
        self.plt_map.plot(ascontiguousarray(LLons.T),
                  ascontiguousarray(LLats.T),
                  color='gray',latlon=True)
        plt.savefig('~test_ground2geo.png')
        plt.close()

    def test_geo2ground(self):
        xg = linspace(0.001, 425, 25)
        yg = linspace(0, 700, 30)
        xxg, yyg = meshgrid(xg, yg)
        
        LLons, LLats = self.fm.ground2geo(xxg, yyg)

        xxg1, yyg1 = self.fm.geo2ground(LLons, LLats)

        assert_almost_equal(xxg, xxg1)
        assert_almost_equal(yyg, yyg1)

    def test_fault2geo(self):
        xf = linspace(0.001, 424.9, 25)
        yf = linspace(0, 700, 30)
        xxf, yyf = meshgrid(xf, yf)
        
        LLons, LLats = self.fm.fault2geo(xxf, yyf)

        self.plt_map.plot(LLons,LLats,color='gray',latlon=True)
        self.plt_map.plot(ascontiguousarray(LLons.T),
                  ascontiguousarray(LLats.T),
                  color='gray',latlon=True)
        plt.savefig('~test_fault2geo.png')
        plt.close()

    def test_geo2fault(self):
        xf = linspace(0.001, 424.9, 25)
        yf = linspace(0, 700, 30)
        xxf, yyf = meshgrid(xf, yf)
        
        LLons, LLats = self.fm.fault2geo(xxf, yyf)

        xxf1, yyf1 = self.fm.geo2fault(LLons, LLats)

        assert_almost_equal(xxf1, xxf)
        assert_almost_equal(yyf1, yyf)
        
if __name__ == '__main__':
    unittest.main()
