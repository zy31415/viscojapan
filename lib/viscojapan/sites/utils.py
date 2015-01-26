from os.path import join
import re

from numpy import loadtxt, asarray
import numpy as np
import pyproj as pj

from ..utils import get_this_script_dir
from ..hypocenter import TOHOKU_EPICENTER


__all__ = []


this_file_path = get_this_script_dir(__file__)

epi_lon0 = TOHOKU_EPICENTER[0]
epi_lat0 = TOHOKU_EPICENTER[1]

def get_epi_dist(sites):
    lons, lats = get_pos(sites)
    nsites = len(sites)
    p = pj.Geod(ellps='WGS84')
    az1, az2, dis = p.inv(lons, lats, [epi_lon0]*nsites, [epi_lat0]*nsites)
    return dis
    
def sorted_by_epi_dist(sites):
    dist = get_epi_dist(sites)
    dic1 = {s:d for s, d in zip(sites, dist)}
    tp = sorted(dic1.items(), key=lambda x: x[1], reverse=True)
    sites_sorted = [ii[0] for ii in tp]
    dist_sorted = [ii[1] for ii in tp]
    return sites_sorted, dist_sorted

def get_all_sites():
    tp=loadtxt(sites_file,'4a, 2f')
    return [ii[0] for ii in tp]

def get_sites_seafloor():
    ''' Seafloor sites name start with an understore "_"
'''
    with open(sites_file, 'rt') as fid:
        sites_seafloor = re.findall('^_.{3}', fid.read(),re.M)
    res = [si.encode() for si in sites_seafloor]
    return res





