import pickle

from numpy import asarray, log10

with open('res.pkl', 'rb') as fid:
    res = pickle.load(fid)
    
nsol = asarray([ii[2] for ii in res])
nrough = asarray([ii[3] for ii in res])
nres = asarray([ii[4] for ii in res])

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(log10(nsol), log10(nrough), log10(nres))
ax.set_xlabel('nsol')
ax.set_ylabel('nrough')
ax.set_zlabel('nres')
plt.show()
