from h5py import File

with File('Jac.h5') as fid:
    jac = fid['Jac'][...]

from pylab import *

imshow(jac)
colorbar()
show()
