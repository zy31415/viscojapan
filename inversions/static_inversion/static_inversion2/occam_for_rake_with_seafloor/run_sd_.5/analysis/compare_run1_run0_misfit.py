import glob

import h5py
from pylab import plt

def collect_results(outs_files, key):
    outs = []
    for file in outs_files:
        with h5py.File(file, 'r') as fid:
            out = fid[key][...]
            outs.append(out)
    return outs

files = sorted(glob.glob('../outs/ano_??.h5'))
nrough1 = collect_results(files, 'regularization/roughening/norm')
nres1 = collect_results(files, 'misfit/norm_weighted')


files = sorted(glob.glob('../../run0/outs/ano_??.h5'))
nrough0 = collect_results(files, 'regularization/roughening/norm')
nres0 = collect_results(files, 'misfit/norm_weighted')

plt.loglog(nres0, nrough0, '.', label='Result0')
plt.loglog(nres1, nrough1, '.', label='Result1')
plt.grid('on')
plt.xlabel('norm of weighted residual')
plt.ylabel('norm of solution roughness')
plt.xlim([.7,5])
plt.legend()

plt.savefig('compare_misfit.png')
plt.show()
