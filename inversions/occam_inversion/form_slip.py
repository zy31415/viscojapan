#!/usr/bin/env python3

import sys
import pickle
from os.path import join

from numpy import logspace


sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.post_inversion_form_slip import FormSlip
from viscojapan.inversion.slip import incr_slip_to_slip
from days import days

path_outs = './outs_tik2/'
for ano, alpha in enumerate(logspace(-5,3,30)):
    with open(join(path_outs,'res_%02d.pkl'%ano),'rb') as fid:
        alpha, sol = pickle.load(fid)

    invres = FormSlip()
    invres.solution = sol
    invres.epochs = days
    invres.nlin_par_names = ['log10_visM']

    invres.init()
    info_dic = {'alpha':alpha,
                'tik_order':2,}
    incr_slip_file = join(path_outs, 'incr_slip_%02d.h5'%ano)
    slip_file = join(path_outs, 'slip_%02d.h5'%ano)
    invres.gen_inverted_incr_slip_file(incr_slip_file, info_dic)
    incr_slip_to_slip(incr_slip_file, slip_file)
