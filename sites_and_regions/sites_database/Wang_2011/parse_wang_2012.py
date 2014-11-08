import numpy as np

import viscojapan as vj

def read_file(fn):
    tp = np.loadtxt(fn,'4a, 2f', usecols=(0,1,2))
    return {ii[0].decode():(float(ii[1][0]), float(ii[1][1])) for ii in tp}

sites_TEONET = read_file('Wang_2011_TEONET.txt')
sites_IGSSTA = read_file('Wang_2011_IGS.txt')
 
with open('sites_networks', 'w') as fid:
    for key in sorted(sites_TEONET):
        fid.write('%s TEONET Wang_2011\n'%key)

    for key in sorted(sites_IGSSTA):
        fid.write('%s IGSSTA Wang_2011\n'%key)

sites = sites_TEONET.copy()
sites.update(sites_IGSSTA)

with open('sites_pos', 'w') as fid:
    for key in sorted(sites):
        pos = sites[key]
        fid.write('%s %f %f Wang_2011\n'%(key, pos[0], pos[1]))

    
