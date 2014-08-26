import numpy as np
import pyproj as pj

tp = np.loadtxt('sites_with_seafloor','4a, 2f')
sites = [ii[0] for ii in tp]
lons = [ii[1][0] for ii in tp]
lats = [ii[1][1] for ii in tp]
nsites = len(sites)

pos_dic = {s:(lon,lat) for s, lon, lat in zip(sites, lons, lats)}

lon0 =142.3716
lat0 = 38.2977

p = pj.Geod(ellps='WGS84')
az1, az2, dis = p.inv(lons, lats, [lon0]*nsites, [lat0]*nsites)

dist_dic = {si:di for si, di in zip(sites, dis)}

dist_dic_sorted = sorted(dist_dic.items(), key=lambda x : x[1], reverse=True)

with open('sites_sorted_by_distance','wt') as fid:
    fid.write('# site lon lat dist(km)\n')
    for ii in dist_dic_sorted:
        site = ii[0]
        lon = pos_dic[site][0]
        lat = pos_dic[site][1]
        dist = ii[1]
        fid.write('%s %f %f %f\n'%\
                  (site.decode(), lon, lat, dist/1000.))
