import sys

from numpy import dot, asarray, hstack, logspace
from numpy.linalg import norm
from numpy.random import normal

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.fault.checkerboard import gen_checkerboard_slip
from viscojapan.epochal_data.epochal_sites_data import EpochalG
from viscojapan.least_square.least_square import LeastSquare
from viscojapan.least_square.tikhonov_regularization \
     import TikhonovSecondOrder
from viscojapan.plot_utils import Map

# generate observation 
slip = gen_checkerboard_slip(25, 10)*50

m = slip.reshape((-1,1))

f_G = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
epochal_G = EpochalG(f_G, 'sites')
G = epochal_G.get_epoch_value(0)

d = dot(G,m)

east_error = normal(0,3e-3,(1300,1))
north_error = normal(0,3e-3,(1300,1))
up_error = normal(0,10e-3,(1300,1))
error = hstack((east_error, north_error, up_error))
error_flat = error.flatten().reshape([-1,1])

d += error_flat

# inversion:
tik = TikhonovSecondOrder()
tik.nrows_slip = 10
tik.ncols_slip = 25
tik.row_norm_length = 1
tik.col_norm_length = 28./23.03
tik.num_epochs = 1
tik.num_nlin_pars = 0

results_norms = []
roughnesses = []
for alpha in logspace(-10,1,40):    
    lst = LeastSquare()
    lst.G = G
    lst.d = d
    lst.alpha = alpha
    lst.regularization_matrix = tik()

    sol = lst()
    m_inverted = asarray(sol['x'])

    roughness = dot(dot(m_inverted.T,lst.regularization_matrix.todense())
                    ,m_inverted)
    roughness = roughness[0,0]
    roughnesses.append(roughness)

    dm = m - m_inverted
    results_norm = norm(dm)
    results_norms.append(results_norm)

import pickle
with open('L-curve.pkl','wb') as fid:
    pickle.dump((results_norms, roughnesses),fid)


