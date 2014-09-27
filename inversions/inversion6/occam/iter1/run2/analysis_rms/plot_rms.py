import glob

import h5py
from pylab import plt

from epochs import epochs

files = sorted(glob.glob('../outs/*'))
for no, file in enumerate(files):
    with h5py.File(file, 'r') as fid:
        rms = fid['misfit/rms_inland_at_epoch'][...]
    #if no==0:
    plt.plot(epochs, rms,'x-', label='Nrough=%d'%no)
    #plt.plot(epochs, rms,'x-')
    
plt.grid('on')
plt.xlabel('days after mainshock')
plt.ylabel('RMS(m)')
plt.legend(prop={'size':7}, bbox_to_anchor=(0.18, 1.01))
plt.savefig('RMS_misfits_at_epochs.pdf')
plt.show()
        
