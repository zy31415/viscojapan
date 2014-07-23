import h5py

from pylab import plt

nreses =[]
rakes = []

for ano in range(30):
    with h5py.File('outs/ano_%02d.h5'%ano,'r') as fid:
        nres = fid['residual_norm_weighted'][...]
        nreses.append(nres)

        m = fid['m'][...]
        rakes.append(m[-1])
    
plt.semilogx(nreses, rakes,'o')
plt.show()
