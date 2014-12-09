import numpy as np

tp = np.loadtxt('../../coseismic/sites_seafloor','4a, 4a, 2f, 3f, d')

for ii in tp:
    name = ii[0].decode()
    id = ii[1].decode()
    co = ii[3]

    post = np.loadtxt('./prediction/%s.pred'%name)

    post[:,1:] += co

    np.savetxt('./cumu_post_displacement/%s.cumu'%id, post,
               '%d  %f  %f %f')
    
