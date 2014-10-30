import h5py
import numpy as np

from viscojapan.epochal_data import EpochalData
import viscojapan as vj

with h5py.File('ano_09.h5','r') as fid:
    m0 = fid['m'][...]

mm0 = m0.reshape((11, 35))

mm = np.zeros((13, 35))

mm[0:11,:] = mm0

with vj.EpochalFileWriter('slip0.h5') as fid:
    fid[0] = mm.reshape((-1, 1))
