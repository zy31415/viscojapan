import h5py

from viscojapan.epochal_data import EpochalData

with h5py.File('ano_04.h5','r') as fid:
    m = fid['m'][...]

slip = EpochalData('slip0.h5')
slip[0] = m
