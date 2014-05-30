''' For a non-linear inverison to run, you need this information:
(1) dG versus non-linear parameters
(2) G
(3) slip  - initial value
(4) obs 
'''

import sys

sys.path.append('/home/zy/workspace/greens/lib')
from greens.diff_ed import DiffED
from greens.edr_sites_filtered import EDRSitesFiltered
from greens.jacobian_vector import Jacobian_Vec
from greens.ed_reader import EDReader

sites_file = 'sites'
file_G1 = '../greensfunction/050km-vis00/G.h5'
file_G2 = '../greensfunction/050km-vis01/G.h5'

f_m0 = './model/model.h5'

G1 = EDRSitesFiltered(file_G1, sites_file)
G2 = EDRSitesFiltered(file_G2, sites_file)

dG = DiffED(G1, G2, 'log10_visM')

m0 = EDReader(f_m0)

jacobian_vec = Jacobian_Vec(dG, m0)

