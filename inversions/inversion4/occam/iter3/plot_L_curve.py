import h5py
import matplotlib

from viscojapan.plots import plot_L, plt

nreses =[]
nroughs = []

for ano in range(20):
    with h5py.File('outs/ano_%02d.h5'%ano,'r') as fid:
        nres = fid['residual_norm_weighted'][...]
        nreses.append(nres)
        nrough = fid['regularization/roughening/norm'][...]
        nroughs.append(nrough)
    
plot_L(nreses, nroughs)

plt.xlim([305, 311])
plt.gca().set_xticks(range(305,311))
plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.ylabel('rake')
plt.xlabel('Residual Norm')
plt.grid('on')

plt.show()
