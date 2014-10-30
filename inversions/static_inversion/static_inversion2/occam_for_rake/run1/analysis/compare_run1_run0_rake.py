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
rake1 = collect_results(files, 'nlin_pars/rake')
nres1 = collect_results(files, 'misfit/norm_weighted')


files = sorted(glob.glob('../../run0/outs/ano_??.h5'))
rake0 = collect_results(files, 'nlin_pars/rake')
nres0 = collect_results(files, 'misfit/norm_weighted')

plt.semilogx(nres0, rake0, '.', label='Result0')
plt.semilogx(nres1, rake1, '.', label='Result1')
plt.grid('on')
plt.xlabel('weighted residual norm')
plt.ylabel('rake')
plt.xlim([.7,5])
plt.legend()

plt.savefig('compare_rake.png')
plt.show()
