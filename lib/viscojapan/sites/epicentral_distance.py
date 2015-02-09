import pyproj as pj

from ..constants import TOHOKU_EPICENTER

__author__ = 'zy'
__all__ = ['get_epicentral_distance', 'sorted_by_epicentral_distance']

epi_lon0 = TOHOKU_EPICENTER[0]
epi_lat0 = TOHOKU_EPICENTER[1]

def get_epicentral_distance(site):
    try:
        sites = site
        return [get_epicentral_distance(site) for site in sites]
    except TypeError:
        p = pj.Geod(ellps='WGS84')
        az1, az2, dis = p.inv(site.lon, site.lat,
                              epi_lon0, epi_lat0)
        dis /=1000. # m => km
        return dis

def sorted_by_epicentral_distance(sites):
    dist = get_epicentral_distance(sites)
    dic1 = {s:d for s, d in zip(sites, dist)}
    tp = sorted(dic1.items(), key=lambda x: x[1], reverse=True)
    sites_sorted = [ii[0] for ii in tp]
    dist_sorted = [ii[1] for ii in tp]
    return sites_sorted, dist_sorted