import glob

from pylab import plt
import numpy as np

import viscojapan as vj

from epochs import epochs

files = sorted(glob.glob('../outs/outs_????/rough_16.h5'))

fault_file = '../../fault_model/fault_bott80km.h5'

rmses = []
for file in files:
    reader = vj.inv.ResultFileReader(file)
    rms = reader.rms_inland
    rmses.append(rms)
   
reader = vj.inv.ResultFileReader('../../../run0/outs/nrough_06_naslip_11.h5')
rmses_combo = reader.rms_inland_at_epoch

plt.plot(epochs, np.asarray(rmses)*100,'--^',
         label='Afterslip only model')
plt.plot(epochs, np.asarray(rmses_combo)*100,'--o',
         label='Coupled viscoelastic + afterslip model')
plt.xlabel('days after the mainshock')
plt.ylabel('RMS misfit (cm)')
plt.grid('on')
plt.legend(loc=8, prop={'size':12})
plt.savefig('misfits_static_vs_combo.pdf')
plt.show()
