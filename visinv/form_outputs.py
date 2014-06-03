import sys
import pickle

from numpy import logspace

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.post_inversion import InversionResults
from viscojapan.slip import incr_slip_to_slip
from days import days

for ano, alpha in enumerate(logspace(-5,3,30)):
    with open('outs/res_%02d.pkl'%ano,'rb') as fid:
        alpha, sol = pickle.load(fid)

    invres = InversionResults()
    invres.solution = sol
    invres.epochs = days
    invres.nlin_par_names = ['log10_visM']

    invres.init()
    info_dic = {'alpha':alpha}
    incr_slip_file = 'outs/incr_slip_%02d.h5'%ano
    slip_file = 'outs/slip_%02d.h5'%ano
    invres.gen_inverted_incr_slip_file(incr_slip_file, info_dic)
    incr_slip_to_slip(incr_slip_file, slip_file)
