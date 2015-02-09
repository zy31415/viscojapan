import numpy as np

from point_in_polygon import Polygon

__author__ = 'zy'
__all__ = ['choose_sites_in_polygon']

def choose_sites_in_polygon(sites,x,y):
    p = Polygon(x,y)
    ch = []
    for lon, lat in zip(sites.lons, sites.lats):
        mindst = p.is_inside(lon, lat)
        if mindst < 0:
            ch.append(False)
        else:
            ch.append(True)
    return np.asarray(ch)
