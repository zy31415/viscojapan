from h5py import File

with File('a.h5') as fid:
    fid['info/a']=1
    fid['info/b']=2

