import sys
from os.path import join

from numpy import logspace, vstack
from numpy.linalg import norm
import h5py

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.ed_sites_filtered import EDSitesFiltered
from viscojapan.epochal_data import EpochalData
from viscojapan.stacking import vstack_column_vec
from viscojapan.tikhonov_regularization import TikhonovSecondOrder

from days import days as epochs

alphas = logspace(-5,3,30)

file_obs = 'cumu_post.h5'
dir_outs = 'outs_tik2'
file_sites = 'sites'

obs = EDSitesFiltered(file_obs, file_sites)

solution_norms=[]

for ano, alpha in enumerate(alphas):
    fn = join(dir_outs,'pred_disp_%02d.h5'%ano)
    pred = EpochalData(fn)
    epochs = pred.get_epochs()

    d1 = vstack_column_vec(pred, epochs)
    d2 = vstack_column_vec(obs, epochs)
    solution_norm = norm(d1-d2)
    solution_norms.append(solution_norm)


reg = TikhonovSecondOrder(nrows_slip=10, ncols_slip=25)
reg.row_norm_length = 1
reg.col_norm_length = 28./23.03
reg.num_epochs = len(epochs)
reg.num_nlin_pars = 1
reg_mat = reg.regularization_matrix()

roughness = []

for ano, alpha in enumerate(alphas):
    fn = join(dir_outs,'incr_slip_%02d.h5'%ano)
    incr_slip = EpochalData(fn)
    m = vstack_column_vec(incr_slip, epochs)
    m = vstack([m,[0]])

    raise ValueError('This is wrong, because reg_mat here is L^T*L, not L')
    roughness.append(norm(reg_mat.dot(m)))

with h5py.File('L-curve.h5') as fid:
    fid['solution_norms'] = solution_norms
    fid['roughness'] = roughness

    
