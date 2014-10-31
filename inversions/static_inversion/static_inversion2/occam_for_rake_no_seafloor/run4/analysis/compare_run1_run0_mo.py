import glob

import h5py
from pylab import plt

import viscojapan as vj

def collect_results(outs_files, key):
    outs = []
    for file in outs_files:
        with h5py.File(file, 'r') as fid:
            out = fid[key][...]
            outs.append(out)
    return outs

com  = vj.ComputeMoment('../../../fault_model/fault_bott60km.h5',
                        '../earth.model_He63km_VisM1.0E19'
                        )

files = sorted(glob.glob('../outs/ano_??.h5'))
Bm1 = collect_results(files, 'Bm')
slip1 = [ii[:-1, :] for ii in Bm1]
mo1 = [com.moment(ii)[0] for ii in slip1]

nres1 = collect_results(files, 'misfit/norm_weighted')


files = sorted(glob.glob('../../run0/outs/ano_??.h5'))
Bm0 = collect_results(files, 'Bm')
slip0 = [ii[:-1, :] for ii in Bm0]
mo0 = [com.moment(ii)[0] for ii in slip0]

nres0 = collect_results(files, 'misfit/norm_weighted')

plt.semilogx(nres0, mo0, '.', label='Result0')
plt.semilogx(nres1, mo1, '.', label='Result1')
plt.grid('on')
plt.xlabel('norm of weighted residual')
plt.ylabel('Mo')
plt.xlim([.7,5])
plt.legend()

plt.savefig('compare_mo.png')
plt.show()
