import h5py

from viscojapan.plots import plot_L, plt

from alphas import alphas

nreses =[]
nroughs = []

for ano in range(30):
    with h5py.File('outs/ano_%02d.h5'%ano,'r') as fid:
        nres = fid['residual_norm_weighted'][...]
        nreses.append(nres)
        nrough = fid['regularization/roughening/norm'][...]
        nroughs.append(nrough)
    
plot_L(nreses, nroughs, alphas)
plt.show()
