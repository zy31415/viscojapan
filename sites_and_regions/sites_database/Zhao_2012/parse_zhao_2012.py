import numpy as np

import viscojapan as vj

def read_file(fn):
    tp = np.loadtxt(fn,'2f, 4a', usecols=(0,1,6))
    return {ii[1].decode():(float(ii[0][0]), float(ii[0][1])) for ii in tp}

sites_CMONOC = read_file('Zhao_2012_CMONOC.txt')
sites_IGSSTA = read_file('Zhao_2012_IGS.txt')
 
with open('sites_networks', 'w') as fid:
    for key in sorted(sites_CMONOC):
        fid.write('%s CMONOC Zhao_2012\n'%key)

    for key in sorted(sites_IGSSTA):
        fid.write('%s IGSSTA Zhao_2012\n'%key)

sites = sites_CMONOC.copy()
sites.update(sites_IGSSTA)

with open('sites_pos', 'w') as fid:
    for key in sorted(sites):
        pos = sites[key]
        fid.write('%s %f %f Zhao_2012\n'%(key, pos[0], pos[1]))

    
