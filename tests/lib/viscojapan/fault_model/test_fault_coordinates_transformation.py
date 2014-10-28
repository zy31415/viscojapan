import unittest
from os.path import join
import warnings

from numpy import arange, meshgrid, ascontiguousarray, linspace
from numpy.testing import assert_almost_equal, assert_array_almost_equal
from pylab import plt

from viscojapan.fault_model.transform import FaultCoordinatesTransformation
from viscojapan.fault_model.control_points import control_points2
from viscojapan.utils import get_this_script_dir
from viscojapan.plots.map_plot import MapPlot

this_test_path = get_this_script_dir(__file__)

class TestFaultCoordinatesTransformation(unittest.TestCase):
    def setUp(self):
        self.fm = FaultCoordinatesTransformation(control_points2)

        self.plt_map = MapPlot()

    def test__lonlat_to_xy(self):
        B0 = self.fm.B0
        xgc, ygc = self.fm._lonlat_to_xy(B0[0], B0[1])
        self.assertEqual(xgc,0)
        self.assertEqual(ygc,0)

    def test_xy_lonlat(self):
        A = (142.1, 34.8)
        lons = linspace(self.fm.B0[0], A[0], 20)
        lats = linspace(self.fm.B0[1], A[1], 20)

        xgc, ygc = self.fm._lonlat_to_xy(lons, lats)

        lons1, lats1 = self.fm._xy_to_lonlat(xgc, ygc)

        assert_array_almost_equal(lons, lons1)
        assert_array_almost_equal(lats, lats1)

    def test_ground2geo(self):
        xp = linspace(0, 700, 25)
        yp = linspace(0, 425, 30)
        xxp, yyp = meshgrid(xp, yp)
       
        LLons, LLats = self.fm.ground2geo(xxp, yyp)

        self.plt_map.basemap.plot(LLons,LLats,color='gray',latlon=True)
        self.plt_map.basemap.plot(ascontiguousarray(LLons.T),
                  ascontiguousarray(LLats.T),
                  color='gray',latlon=True)
        plt.savefig('~test_ground2geo.png')
        plt.close()
##
    def test_geo2ground(self):
        xp = linspace(0.,700, 25)
        yp = linspace(0, 425, 30)
        xxp, yyp = meshgrid(xp, yp)
        
        LLons, LLats = self.fm.ground2geo(xxp, yyp)

        xxp1, yyp1 = self.fm.geo2ground(LLons, LLats)

        assert_almost_equal(xxp, xxp1)
        assert_almost_equal(yyp, yyp1)

    def test_fault2ground_ground2fault(self):
        xf = linspace(0,700, 10)
        yf = linspace(0, 425, 15)
        xf, yf = meshgrid(xf, yf)

        xp, yp = self.fm.fault2ground(xf, yf)
        xf1, yf1 = self.fm.ground2fault(xp, yp)
        
        assert_almost_equal(xf, xf1)
        assert_almost_equal(yf, yf1)
        
##
    def test_fault2geo(self):
        xf = linspace(0., 700, 25)
        yf = linspace(0, 425, 30)
        xxf, yyf = meshgrid(xf, yf)
        
        LLons, LLats = self.fm.fault2geo(xxf, yyf)

        self.plt_map.basemap.plot(LLons,LLats,color='gray',latlon=True)
        self.plt_map.basemap.plot(ascontiguousarray(LLons.T),
                  ascontiguousarray(LLats.T),
                  color='gray',latlon=True)
        plt.savefig('~test_fault2geo.png')
        plt.close()

    

    def test_geo2fault(self):
        xf = linspace(0., 700, 15)
        yf = linspace(0, 425, 10)
        xxf, yyf = meshgrid(xf, yf)
        
        LLons, LLats = self.fm.fault2geo(xxf, yyf)

        xxf1, yyf1 = self.fm.geo2fault(LLons, LLats)

        assert_almost_equal(xxf1, xxf)
        assert_almost_equal(yyf1, yyf)
        
if __name__ == '__main__':
    unittest.main()
