#!/usr/bin/env python3

import sys
import pickle
from os.path import join

from numpy import logspace

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.post_inversion import InversionResults
from viscojapan.slip import incr_slip_to_slip
from viscojapan.formulate_occam import FormulatOccam
from viscojapan.jacobian_vec import JacobianVec
from viscojapan.ed_sites_filtered import EDSitesFiltered
from viscojapan.diff_ed import DiffED
from viscojapan.epochal_data import EpochalData
from viscojapan.invert import Invert
from viscojapan.post_inversion import InversionResults
from viscojapan.tikhonov_regularization import TikhonovSecondOrder
from days import days as epochs
from days import days

sites_file = 'sites'

file_G1 = '../greensfunction/050km-vis02/G.h5'
G1 = EDSitesFiltered(file_G1, sites_file)

file_G2 = '../greensfunction/050km-vis01/G.h5'
G2 = EDSitesFiltered(file_G2, sites_file)

dG = DiffED(G1, G2, 'log10_visM')


f_d = 'cumu_post.h5'
obs = EDSitesFiltered(f_d, sites_file)

visM = G1.get_info('visM')
log10_visM = log10(visM)
print('Initial Maxwellian viscosity: %g'%visM)

f_slip0 = 'slip0.h5'
jac_1 = JacobianVec(dG, f_slip0)

# FormulatOccam 
form = FormulatOccam()
form.epochs = epochs
form.non_lin_par_vals = [log10_visM]
form.non_lin_JacobianVecs = [jac_1]
form.G = G1
form.d = obs


path_outs = './outs_tik2/'
for ano, alpha in enumerate(logspace(-5,3,30)):
    with open(join(path_outs,'res_%02d.pkl'%ano),'rb') as fid:
        alpha, sol = pickle.load(fid)

    invres = InversionResults()
    invres.solution = sol
    invres.epochs = days
    invres.nlin_par_names = ['log10_visM']
    invres.nllin_par_vals0 = 18.76640079973536
    invres.G = form.G
    invres.d = form.G
    invres.num_obs = 1300
    invres.file_pre = join(path_outs,'pred_obs%02d.h5'%ano)

    invres.init()
    info_dic = {'alpha':alpha,
                'tik_order':2,}
    incr_slip_file = join(path_outs, 'incr_slip_%02d.h5'%ano)
    slip_file = join(path_outs, 'slip_%02d.h5'%ano)
    invres.gen_inverted_incr_slip_file(incr_slip_file, info_dic)
    incr_slip_to_slip(incr_slip_file, slip_file)

    invres.get_predicated_obs()
