import h5py
import numpy as np

from viscojapan.epochal_data import EpochalData
import viscojapan as vj

with h5py.File('ano_09.h5','r') as fid:
    m0 = fid['m'][...][:-1,:]

mm = m0.reshape((13, 35))

with vj.EpochalFileWriter('slip0.h5') as fid:
    fid[0] = mm.reshape((-1, 1))
