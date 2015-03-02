import numpy as np

import glob

files = sorted(glob.glob('outs/*'))

sites = np.loadtxt('near_stations.in','4a', usecols=(0,))
sites = [site.decode() for site in sites]

def load(fn, site, cmpt):
    idx = sites.index(site)
    if cmpt=='e':
        c = 2
    return np.loadtxt(fn)[idx,c]


def get_ts(site, cmpt):
    epochs = []
    ys = []
    for f in files:
        epochs.append(int(f.split('_')[-3]))
        ys.append(load(f,site,cmpt))

    return epochs, ys



site = 'J550'

epochs, ys = get_ts(site, 'e')

from pylab import plt

plt.plot(epochs[1:],ys[1:])
plt.show()
