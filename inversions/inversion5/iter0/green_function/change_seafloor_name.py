import numpy as np
import h5py

seafloor_file = '/home/zy/workspace/viscojapan/tsana/sea_floor/sites_seafloor'
tp = np.loadtxt(seafloor_file,'4a, 4a, 2f, 3f, d')
from_to = {ii[0]:ii[1] for ii in tp}

def switch(from_to, sites):
    for s1, s2 in from_to.items():
        sites = list(sites)
        if s1 in sites:
            idx = sites.index(s1)
            sites[idx] = s2
    return sites

def change_sites_in_epochal_file(ep_file):
    with h5py.File(ep_file) as fid:
        sites = fid['info/sites'][...]
        sites = switch(from_to, sites)
        del fid['info/sites']
        fid['info/sites'] = sites

for ep_file in ['./G_He40km_Vis1.1E19_Rake83.h5',
                './G_He40km_Vis5.8E18_Rake83.h5',
                './G_He40km_Vis5.8E18_Rake90.h5',
                './G_He45km_Vis5.8E18_Rake83.h5',
                ]:
    change_sites_in_epochal_file(ep_file)
