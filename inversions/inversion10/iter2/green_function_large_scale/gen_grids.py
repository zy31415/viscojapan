import viscojapan as vj

import numpy as np

north = 80
south = 12
east = 200
west = 80
dx = 200e3
dy = 200e3
grids = vj.make_grids(north, south, west, east, dx, dy)
sites_id = ['X%03X'%ii for ii in range(len(grids))]
_txt = np.array([(s, p[0], p[1]) for s, p in zip(sites_id, grids)],
                dtype = ('U4, f, f'))
np.savetxt('sites.in', _txt, fmt='%s %f %f')



    
    
    
    
    
