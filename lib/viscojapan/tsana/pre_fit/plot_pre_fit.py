import re
from os.path import basename

from numpy import loadtxt, asarray, inf
from pylab import plt

from ..utils import cut_ts

_adj_dates = 678577

def read_linsec(fn):
    with open(fn,'rt') as fid:
        outs = re.findall('.*linear sec.*',fid.read())
    res = []
    for out in outs:            
        linsec = out.split(':')[1].split()
        assert len(linsec)==2
        t1 = linsec[0]
        t2 = linsec[1]
        if t1 == '-inf':
            t1 = -9999
        if t2 == 'inf':
            t2 = 9999999999
        res.append((int(t1),int(t2)))
    return res

def read_outlier(fn):
    with open(fn,'rt') as fid:
        out = re.findall('.*outliers.*',fid.read())[0]

    outlier = out.split(":")[1].split()
    return [int(ii) for ii in outlier]

def outlier_index(t,outliers):
    return [list(t).index(oi) for oi in outliers]

def read_jumps(fn):
    with open(fn,'rt') as fid:
        out = re.findall('^#.*jump:.*',fid.read(),re.M)
    return [int(ii.split(':')[1]) for ii in out]

def plot_pre(fn):
    tp = loadtxt(fn)
    t = asarray(tp[:,0], int)
    y = tp[:,1]
    yres = tp[:,2]

    plt.plot_date(t+_adj_dates, y, 'x', color='lightblue')
    plt.plot_date(t+_adj_dates, yres, 'x', color='lightgreen')

    linsec = read_linsec(fn)

    ch = cut_ts(t, linsec)
    
    plt.plot_date(t[ch]+_adj_dates, y[ch], 'x', color='blue', label='original')
    plt.plot_date(t[ch]+_adj_dates, yres[ch], 'x', color='green', label='residual')

    outliers = read_outlier(fn)
    idx = outlier_index(t, outliers)

    plt.plot_date(t[idx]+_adj_dates, y[idx], 'o', mec='red', mew=1, mfc='blue')
    plt.plot_date(t[idx]+_adj_dates, yres[idx], 'o', mec='red', mew=1, mfc='green')

    for jump in read_jumps(fn):
        plt.axvline(jump + _adj_dates, color='red', ls='--')

    plt.grid('on')
    site = basename(fn).split('.')[0]
    cmpt = basename(fn).split('.')[1]
    plt.title('%s - %s'%(site, cmpt))
    

    
    
