import glob

import numpy as np
from pylab import plt
import h5py

from epochs import epochs

def read_inland_rms_from_files(files):
    rms = []        
    for file in files:
        with h5py.File(file) as fid:
            rms.append(fid['residual_rms_inland'][...])
    return np.asarray(rms)

for nrough in range(30):
    files = sorted(glob.glob('../outs/epoch_????_rough_%02d.h5'%nrough))
    rms = read_inland_rms_from_files(files)
    plt.plot(epochs, rms*100., 'o-')

plt.xlabel('days after the mainshock')
plt.ylabel('RMS misfit (cm)')
plt.grid('on')
plt.title('Slip only RMS misfit')
plt.savefig('rms_slip_only.png')
plt.show()
