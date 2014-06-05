import sys
from os.path import join

from numpy import logspace
from numpy.linalg import norm

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.ed_sites_filtered import EDSitesFiltered
from viscojapan.epochal_data import EpochalData
from viscojapan.stacking import vstack_column_vec

alphas = logspace(-5,3,30)

file_obs = 'cumu_post.h5'
dir_outs = 'outs_tik2'
file_sites = 'sites'

obs = EDSitesFiltered(file_obs, file_sites)

for ano, alpha in enumerate(logspace(-5,3,30)):
    fn = join(dir_outs,'pred_disp_%02d.pkl'%ano)
    print(fn)
    pred = EpochalData(fn)
    epochs = pred.get_epochs()

    d1 = vstack_column_vec(pred, epochs)
    d2 = vstack_column_vec(obs, epochs)
    solution_norm = norm(d1-d2)
    print(solution_norm)
