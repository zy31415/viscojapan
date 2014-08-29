import glob
from os.path import basename

import h5py
import numpy as np

import viscojapan as vj

files = glob.glob('../outs/nsd_??_rough_10_top_02*')

file_sites_filter = '../../sites_with_seafloor'

obj = vj.EpochalDisplacement('../../cumu_post_with_seafloor.h5', file_sites_filter)
d_obs = obj[0]

obj = vj.EpochalDisplacementSD('../../sd_seafloor/sd_files/sd_with_seafloor_00.h5', file_sites_filter)
sd = obj[0]

sites = np.loadtxt(file_sites_filter, '4a')

rmss = []
rms_inlands = []
rms_seafloors = []

for file in sorted(files):
    with h5py.File(file) as fid:
        d_pred = fid['d_pred'][...]
        rms = np.sqrt(np.mean((d_obs - d_pred)**2))
        rms_inland = np.sqrt(np.mean((d_obs[:-15,0] - d_pred[:-15,0])**2))
        rms_seafloor = np.sqrt(np.mean((d_obs[-15:,0] - d_pred[-15:,0])**2))

        rmss.append(rms)
        rms_inlands.append(rms_inland)
        rms_seafloors.append(rms_seafloor)

rmss = np.asarray(rmss)*100.
rms_inlands = np.asarray(rms_inlands)*100.
rms_seafloors = np.asarray(rms_seafloors)*100.

import sys
sys.path.append('../../sd_seafloor/')
from sds import sds

sds = sds*100.
from pylab import plt



plt.subplot(311)
plt.semilogx(sds, rmss, 'o-')
plt.gca().set_xticklabels([])
plt.ylabel(r'$\bf{RMS}/cm$')
plt.grid('on')

plt.subplot(312)
plt.semilogx(sds, rms_inlands, 'o-')
plt.gca().set_xticklabels([])
plt.ylabel(r'$\bf{RMS}_{\bf{inland}}/cm$')
plt.grid('on')

plt.subplot(313)
plt.semilogx(sds, rms_seafloors, 'o-')
plt.ylabel(r'$\bf{RMS}_{\bf{seafloor}}/cm$')
plt.grid('on')

plt.xlabel('SD of seafloor obs.(cm)')
plt.savefig('how_sd_seafloor_affect_goodness_fit.png')
plt.savefig('how_sd_seafloor_affect_goodness_fit.pdf')
plt.show()


