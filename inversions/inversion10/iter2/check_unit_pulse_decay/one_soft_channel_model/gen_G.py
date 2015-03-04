from glob import glob

import numpy as np

import viscojapan as vj

def get_epochs():
    files = glob('outs/*.out')
    epochs = sorted([int(f.split('_')[-3]) for f in files])
    return epochs

He = 50
visM = 6.3E18
visK = np.inf
rake = 90

files = sorted(glob('outs/*'),
               key = lambda f : int(f.split('_')[-3]),
               )
epochs = []
disps = []
for f in files:
    epoch = int(f.split('_')[-3])
    data = np.loadtxt(f, usecols=(2, 3, 4))

    if epoch == 0:
        data0 = data
    else:
        data += data0

    epochs.append(epoch)    
    disps.append(data)

disps = np.asarray(disps)

sites = np.loadtxt('stations.in', '4a', usecols=(0,))
sites = [site.decode() for site in sites]

d = vj.epoch_3d_array.Displacement(disps, epochs, sites)

d.save('disp.h5')

