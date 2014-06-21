import sys
from os.path import exists
import os

import h5py
from numpy import matrix, log10, loadtxt

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.epochal_data import EpochalData

fm = 'incr_slip.h5'

if exists(fm):
    os.remove(fm)

ed = EpochalData(fm)

with h5py.File('co/co.h5', 'r') as fid:
    co = fid['m'][...]
co = matrix(co).T
ed.set_epoch_value(0,co)

with h5py.File('aslip/aslip.h5', 'r') as fid:
    aslip =  fid['m'][...]
aslip = matrix(aslip).T

from days import days

nth = 0
for day in days[1:]:
    m = aslip[nth*250 : (nth+1)*250]
    ed.set_epoch_value(day, m)
    nth += 1

visM = 5.8398382410071849E18
ed_model = EpochalData(fm)
ed_model.set_info('visM', visM)
ed_model.set_info('log10_visM',log10(visM))

