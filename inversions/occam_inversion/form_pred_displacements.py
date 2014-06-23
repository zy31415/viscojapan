#!/usr/bin/env python3
import sys

from numpy import logspace

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.inversion import Inversion
from viscojapan.post_inversion_form_pred_displacements import FormPredDisplacements
from days import days as epochs

inv = Inversion()

inv.sites_file = 'sites'
inv.file_G1 = '../greensfunction/050km-vis02/G.h5'
inv.file_G2 = '../greensfunction/050km-vis01/G.h5'
inv.f_d = 'cumu_post.h5'
inv.f_slip0 = 'slip0.h5'
inv.epochs = epochs

alpha = 100
inv.init()
# inv.invert(alpha)
#inv.save_raw('test.pkl')

for ano, alpha in enumerate(logspace(-5,3,30)):
    print(ano, alpha)
    inv.load_raw('outs_tik2/res_%02d.pkl'%ano)
    form_disp = FormPredDisplacements(inv)
    form_disp.num_of_observation = 3900
    form_disp.gen_pred_displacements_file('outs_tik2/pred_disp_%02d.h5'%ano)
