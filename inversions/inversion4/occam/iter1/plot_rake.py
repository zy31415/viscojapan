import h5py

from pylab import plt

nreses =[]
visMs = []
Hes = []
rakes = []

for ano in range(20):
    with h5py.File('outs/ano_%02d.h5'%ano,'r') as fid:
        nres = fid['residual_norm_weighted'][...]
        nreses.append(nres)

        m = fid['m'][...]
        visMs.append(m[-3])
        Hes.append(m[-2])
        rakes.append(m[-1])

plt.subplot(311)    
plt.semilogx(nreses, visMs,'o')

plt.subplot(312)    
plt.semilogx(nreses, Hes,'o')


plt.subplot(313)    
plt.semilogx(nreses, rakes,'o')
plt.show()
