import glob
from os.path import basename

import h5py
import numpy as np

import viscojapan as vj

files = glob.glob('../outs/nsd_??_rough_10_top_02*')

file_sites_filter = '../../sites_with_seafloor'

com = vj.ComputeMoment('../../fault_bott40km.h5',
                       '../../earth.model_He40km_Vis1.1E19')

sites = np.loadtxt(file_sites_filter, '4a')

Mos = []
Mws = []

for file in sorted(files):
    with h5py.File(file) as fid:
        Bm = fid['Bm'][...]
        mo, mw = com.moment(Bm)
        Mws.append(mw)
        Mos.append(mo)
import sys
sys.path.append('../../sd_seafloor/')
from sds import sds

sds = sds*100.
from pylab import plt


plt.plot(sds, Mws, 'o-')
plt.ylabel(r'$\bf{Mw}$')
plt.grid('on')

plt.xlabel('SD of seafloor obs.(cm)')
plt.savefig('how_sd_seafloor_affect_Mw.png')
plt.savefig('how_sd_seafloor_affect_Mw.pdf')
plt.show()
plt.close()


plt.plot(sds, Mos, 'o-')
plt.ylabel(r'$\bf{Mo}$')
plt.grid('on')

plt.xlabel('SD of seafloor obs.(cm)')
plt.savefig('how_sd_seafloor_affect_Mo.png')
plt.savefig('how_sd_seafloor_affect_Mo.pdf')
plt.show()
plt.close()


