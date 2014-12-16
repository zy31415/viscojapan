import numpy as np

import date_conversion as dc

co_file = 'coseismic/sites_seafloor'
tp = np.loadtxt(co_file, '4a, 4a, f, f, f',
                usecols=(0, 1, 4, 5, 6))
co_dic = {ii[1]:(ii[0],(ii[2], ii[3], ii[4])) for ii in tp}

for id, tp in co_dic.items():
    site = tp[0].decode()
    eco = tp[1][0]
    nco = tp[1][1]
    uco = tp[1][2]
    tp = np.loadtxt('postseismic/post_offsets/%s.post'%site)
    ts = dc.asmjd(tp[:,0]) - 55631
    ts = np.insert(ts, 0 , 0)
    
    es = tp[:,1] + eco
    es = np.insert(es, 0 , eco)
    
    ns = tp[:,2] + nco
    ns = np.insert(ns, 0 , nco)
    
    us = tp[:,3] + uco
    us = np.insert(us, 0 , uco)

    _txt = np.asarray([ts, es, ns, us]).T
    np.savetxt('cumu_post/%s.original'%id.decode(), _txt, '%d %f %f %f',
               header='day e n u')
