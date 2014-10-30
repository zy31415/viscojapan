from os.path import join
import re

from numpy import loadtxt, asarray
import numpy as np
import pyproj as pj

from ..utils import get_this_script_dir
from ..epicenter import TOHOKU_EPICENTER

__all__ = ['get_pos_dic', 'get_pos','sites_file',
           'get_epi_dist','sorted_by_epi_dist','get_sites_seafloor',
           'get_maxmin_lonlat','get_sites_in_box','get_all_sites',
           'remove_sites_from','choose_inland_GPS','choose_inland_GPS_for_cmpts']


this_file_path = get_this_script_dir(__file__)

epi_lon0 = TOHOKU_EPICENTER[0]
epi_lat0 = TOHOKU_EPICENTER[1]

sites_file = join(this_file_path, 'share/sites_with_seafloor')

def get_pos_dic():
    ''' Return a dictionary of position of all stations.
'''
    tp=loadtxt(sites_file,'4a, 2f')
    return {ii[0]:ii[1] for ii in tp}

def get_pos(sites):
    lons=[]
    lats=[]
    pos=get_pos_dic()
    for site in sites:
        tp=pos[site]
        lons.append(tp[0])
        lats.append(tp[1])
    return asarray(lons, 'float'),asarray(lats, 'float')

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

def get_maxmin_lonlat():
    tp = np.loadtxt(sites_file,'4a,2f')
    lons = [ii[1][0] for ii in tp]
    lats = [ii[1][1] for ii in tp]

    return np.amin(lons),np.amax(lons), np.amin(lats),np.amax(lats)

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

def get_sites_in_box(box):
    lon1 = box[0]
    lat1 = box[1]
    lon2 = box[2]
    lat2 = box[3]

    pos_dic = get_pos_dic()
    sites = []
    for site, pos in pos_dic.items():
        lon = pos[0]
        lat = pos[1]
        if lon>lon1 and lon<lon2 and lat>lat1 and lat<lat2:
            sites.append(site)
    return sites

def remove_sites_from(sites0, sites1):
    out = []
    for site in sites0:
        if site not in sites1:
            out.append(site)
    return out

def choose_inland_GPS(sites):
    ch = []
    for site in sites:
        if site[0]=='_':
            ch.append(False)
        else:
            ch.append(True)
    return np.asarray(ch,bool)

def choose_inland_GPS_for_cmpts(sites, num_epochs = 1):
    ch = choose_inland_GPS(sites)
    out = np.asarray([[ch]*3]).T.flatten()
    out = np.asarray([out]*num_epochs).flatten()
    return out

