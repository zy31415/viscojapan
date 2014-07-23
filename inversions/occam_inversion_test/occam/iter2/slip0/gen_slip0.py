import h5py

from viscojapan.epochal_data import EpochalData

with h5py.File('ano_00.h5','r') as fid:
    Bm = fid['Bm'][...]

slip = EpochalData('slip0.h5')

# skip nonlinear par value
slip[0] = Bm[0:-1,:]
