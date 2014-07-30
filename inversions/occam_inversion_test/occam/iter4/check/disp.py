import h5py
from numpy import dot
from numpy.linalg import norm

import viscojapan as vj

g = vj.EpochalG('../../../greens_function/G_Rake80.h5')

G = g[0]


with h5py.File('../outs/ano_10.h5','r') as fid:
    Bm = fid['Bm'][...]
slip = Bm[:-1,:]

##with h5py.File('../../../final_slip/outs/ano_10.h5','r') as fid:
##    Bm = fid['Bm'][...]
##slip = Bm

d_pred = dot(G,slip)
print(d_pred)

d_ep = vj.EpochalDisplacement('../../../true_model/d_simu.h5')
d_true = d_ep[0]
print(d_true)
print(norm(d_pred-d_true))
