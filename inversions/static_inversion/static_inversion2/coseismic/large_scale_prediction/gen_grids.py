import viscojapan as vj

import numpy as np

north = 80
south = 12
east = 200
west = 80
dx = 200e3
dy = 200e3
grids = vj.make_grids(north, south, west, east, dx, dy)

np.savetxt('sites.in', grids, fmt='%f  %f')



    
    
    
    
    
