import h5py
import matplotlib

from viscojapan.plots import plot_L, plt

nreses =[]
nroughs = []

for ano in range(20):
    with h5py.File('outs/ano_%02d_bno_10.h5'%ano,'r') as fid:
        nres = fid['residual_norm_weighted'][...]
        nreses.append(nres)
        nrough = fid['regularization/roughening/norm'][...]
        nroughs.append(nrough)
    
plot_L(nreses, nroughs)

xlim = (14, 34)
plt.xlim(xlim)
plt.gca().set_xticks(range(xlim[0],xlim[1]))
plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.grid('on')

plt.savefig('plots/L-curve.png')
plt.show()
