import numpy as np

from viscojapan.utils import _assert_assending_order

tp = np.loadtxt('/home/zy/workspace/viscojapan/tsana/raw_ts/sites/sites','4a,2f')
sites = [ii[0] for ii in tp]
sites_dic = {ii[0]:ii[1] for ii in tp}

tp = np.loadtxt('/home/zy/workspace/viscojapan/tsana/sea_floor/sites_seafloor',
           '4a,4a,2f, 3f, d')
sites += [ii[1] for ii in tp]
_assert_assending_order(sites)
sites_seafloor_dic = {ii[1]:ii[2] for ii in tp}

sites_dic = dict(list(sites_dic.items()) + list(sites_seafloor_dic.items()))

with open('stations.in','wt') as fid:
    fid.write("# This list is used for computing green's function\n")
    fid.write('# num of sites : %d\n'%len(sites))
    fid.write('# site lon lat\n')
    for site in sites:
        pos = sites_dic[site]
        fid.write('%s %f %f\n'%(site.decode(), pos[0], pos[1]))
