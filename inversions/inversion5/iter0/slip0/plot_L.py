from pylab import show, legend, savefig
import h5py
import glob

from viscojapan.plots import plot_L, plt

from alphas import alphas
from betas import betas


files = sorted(glob.glob('outs/ano_??_bno_10.h5'))

nres = []
nrough = []

for file in files:
    with h5py.File(file) as fid:
        nres.append(fid['residual_norm_weighted'][...])
        nrough.append(fid['regularization/roughening/norm'][...])

plot_L(nres, nrough)
plt.savefig('plots/L-curve.png')
plt.show()


