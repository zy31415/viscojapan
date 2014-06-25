import h5py

with h5py.File('sites_data.h5') as fid:
    res = fid['epochs/0001'][0]=999
