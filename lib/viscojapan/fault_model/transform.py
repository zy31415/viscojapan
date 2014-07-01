from numpy import asarray, zeros_like, nan, cos, pi, sin
from pyproj import Proj

from .fault_framework import FaultFramework

class FaultCoordinatesTransformation(FaultFramework):
    """ Coordinates transformations bewteen these three coordinates:
(1) Geo-coordinates expressed by (lon,lat)
(2) Ground coordinates expressed by (east,north) in km
(3) Fault coordinates in km

Fault    <=> Ground   <=> Geo
(xf, yf) <=> (xg, yg) <=> (lon, lat)

"""
    def __init__(self):
        super().__init__()
        self.org_lon = self.B0[0]
        self.org_lat = self.B0[1]

    def _lonlat_to_xy(self, lon, lat):
        lon = asarray(lon)
        lat = asarray(lat)
        
        p=Proj(proj='utm', zone=54, ellps='WGS84')
        x, y = p(lon, lat)

        x0, y0 = p(self.org_lon, self.org_lat)

        x = (x-x0)/1000. # m => km
        y = (y-y0)/1000.
        return  x, y

    def _xy_to_lonlat(self, x, y):
        x = asarray(x)
        y = asarray(y)
        p=Proj(proj='utm', zone=54, ellps='WGS84')
        x0, y0 = p(self.org_lon, self.org_lat)
        x1 = x*1000. + x0
        y1 = y*1000. + y0
        lon, lat = p(x1, y1, inverse = True)
        return lon, lat

    def _rotate_north_to_strike(self, x, y):
        x = asarray(x)
        y = asarray(y)
        alpha = -self.flt_strike*pi/180
        x1 = cos(alpha)*x + sin(alpha)*y
        y1 = -sin(alpha)*x + cos(alpha)*y

        return x1, y1

    def _rotate_strike_to_north(self, x, y):
        x = asarray(x)
        y = asarray(y)
        alpha = self.flt_strike*pi/180.
        x1 = cos(alpha)*x + sin(alpha)*y
        y1 = -sin(alpha)*x + cos(alpha)*y
        return x1,y1

    def fault2ground(self,xf, yf):
        xf = asarray(xf)
        yf = asarray(yf)
        xg = self.xfault_to_xground(xf)
        yg = yf
        return xg, yg

    def ground2fault(self, xg, yg):
        xg = asarray(xg)
        yg = asarray(yg)
        xf = self.xground_to_xfault(xg)
        yf = yg
        return xf, yf

    def ground2geo(self, xg, yg):
        x1, y1 = self._rotate_strike_to_north(xg, yg)
        lon, lat = self._xy_to_lonlat(x1, y1)
        return lon, lat

    def geo2ground(self, lon, lat):
        x, y = self._lonlat_to_xy(lon, lat)
        x1, y1 = self._rotate_north_to_strike(x, y)
        return x1, y1
        
    def fault2geo(self, xf, yf):
        xg, yg = self.fault2ground(xf, yf)
        lon, lat = self.ground2geo(xg, yg)
        return lon,lat

    def geo2fault(self, lon, lat):
        x, y = self.geo2ground(lon, lat)
        x1, y1 = self.ground2fault(x, y)
        return x1, y1
