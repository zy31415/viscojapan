import h5py

with h5py.File('test_data.h5','r') as fid:
    arr = fid['data'][...]

idx = range(100)
for nth in range(60):
    arr[idx,:,:]
        
