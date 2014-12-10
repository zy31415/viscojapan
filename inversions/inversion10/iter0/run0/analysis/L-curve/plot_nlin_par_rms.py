import glob

import h5py
from pylab import plt
from numpy import log10, amin, amax
import matplotlib

import viscojapan as vj

files = sorted(glob.glob('../../outs/*.h5'))

vj.inv.plot_L_curve(files)
plt.savefig('L-curve.png')
plt.show()
