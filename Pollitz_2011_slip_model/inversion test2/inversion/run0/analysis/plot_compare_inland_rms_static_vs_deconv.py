import glob
import pickle

import numpy as np
from pylab import plt
import h5py

from epochs import epochs

def read_inland_rms_from_files(files):
    rms = []        
    for file in files:
        with h5py.File(file) as fid:
            rms.append(fid['misfit/rms_inland'][...])
    return np.asarray(rms)

nrough = 10
files = sorted(glob.glob('../outs/epoch_????_rough_%02d.h5'%nrough))
rms = read_inland_rms_from_files(files)
plt.plot(epochs, rms*100., 'o-', label='RMS (afterslip only model)')

with open('rms_deconv.pkl','rb') as fid:
    t,y = pickle.load(fid)

plt.plot(t, np.asarray(y)*100., 'o-', label='RMS (afterslip + viscoelastic relax.)')

plt.xlabel('days after the mainshock')
plt.ylabel('RMS misfit (cm)')
plt.grid('on')
plt.title('Slip only RMS misfit')
plt.legend(loc=0)
plt.savefig('rms_static_vs_deconv.png')
plt.show()
