import pickle

from viscojapan.plots import plot_L, plt

with open('res.pkl', 'rb') as fid:
    res = pickle.load(fid)

nrough = [ii[1] for ii in res]
nres = [ii[2] for ii in res]

plot_L(nres, nrough)
plt.show()
