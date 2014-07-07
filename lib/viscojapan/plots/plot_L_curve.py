import glob

import h5py
from pylab import loglog, xlabel, ylabel, grid, text

def plot_L_from_res_h5(pathname, x_key, y_key, **kwargs):
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

def plot_L(nres,nsol,alphas=None,lanos=None,
           label=None,color='blue'):
    '''
alphas - regularization parameters array
lanos - array that indicates which alphas pairs are labeled.
        None means label every two.
label - L-curve label
'''
    assert len(nres)==len(nsol)
    if alphas is not None:
        assert len(nres)==len(alphas)
    # plot L-curve
    loglog(nres,nsol,'o-',label=label,color=color)

    if alphas is not None:
        if lanos is None:
            lanos = range(0,len(alphas),2)
        for ano in lanos:
            text(nres[ano],nsol[ano],'%d/%.2G'%(ano,alphas[ano]),color='red')

    xlabel('Residual Norm ($\log_{10}{||Gm-d||_2}$)')
    ylabel('Solution Roughness ($\log_{10}{||Lm||_2}$)')
    grid('on')
