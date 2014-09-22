import numpy as np
import pyproj

import viscojapan as vj

pos_dic = vj.get_pos_dic()

tp = np.loadtxt('ozawa_2011.txt')
ids = np.asarray(tp[:,0], int)
lats = tp[:,3]
lons = tp[:,4]
es = tp[:,5]
ns = tp[:,6]
us = tp[:,7]

id_sites = {}
id_not_found = []
g = pyproj.Geod(ellps='WGS84')

def found_name(lon,lat):
    for site, (lon0, lat0) in pos_dic.items():
        az1, az2, dist = g.inv(lon,lat, lon0, lat0)
        if dist<100:
            return site
    return None

for ii, lon, lat, ei, ni, ui in zip(ids, lons, lats, es, ns, us):
    site = found_name(lon,lat)
    if site is None:
        print('%d Not found!'%ii)
        id_not_found.append(ii)
    else:
        id_sites[site] = (ei, ni, ui)

sites = sorted(id_sites.keys())

with open('ozawa_2011_obs_file','w') as fid:
    fid.write('# site es ns us\n')
    for site in sites:
        ei, ni, ui = id_sites[site]
        fid.write('%s  %f  %f  %f\n'%(site.decode(), ei, ni, ui))
        
with open('sites_ozawa','w') as fid:
    fid.write('%s\n'%site.decode())
    
        
    
