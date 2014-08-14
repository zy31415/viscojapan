import sys

import h5py

import viscojapan as vj

sys.path.append('../')
from epochs_log import epochs 

f_res = 'outs/bno_04_cno_06.h5'
fault_file = '../fault_model/fault_bott40km.h5'

fid = vj.FaultFileIO(fault_file)

num_subflt_along_strike = fid.num_subflt_along_strike
num_subflt_along_dip = fid.num_subflt_along_dip
num_subflts = num_subflt_along_strike * num_subflt_along_dip

num_epochs = len(epochs)
num_nlin_pars = 3

with h5py.File(f_res) as fid:
    Bm = fid['Bm'][...]

slip = Bm[:-num_nlin_pars].reshape([num_epochs,num_subflt_along_dip, num_subflt_along_strike])

from pylab import plt

plt.pcolor(slip[0])
plt.show()
