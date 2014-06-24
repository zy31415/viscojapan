import glob

import h5py
from pylab import loglog, xlabel, ylabel, grid

def plot_L(pathname, x_key, y_key, **kwargs):
    flist = glob.glob(pathname)
    flist = sorted(flist)

    xs = []
    ys = []
    
    for f in flist:
        with h5py.File(f,'r') as fid:
            x = fid[x_key][...]
            y = fid[y_key][...]
        xs.append(x)
        ys.append(y)

    handle = loglog(xs,ys, **kwargs)
    xlabel(x_key)
    ylabel(y_key)
    grid('on')
    return handle
