import re

from numpy import loadtxt
from pylab import plt

from ..utils import cut_ts

_adj_dates = 678577

def read_linsec(fn):
    with open(fn,'rt') as fid:
        out = re.findall('.*linear sec.*',fid.read())[0]
    linsec = out.split(':')[1].split()
    res = []
    for nth, t1 in enumerate(linsec[::2]):
        t2 = linsec[nth*2+1]
        res.append((t1,t2))
    return res

def read_outlier(fn):
    with open(fn,'rt') as fid:
        out = re.findall('.*linear sec.*',fid.read())
    

def plot_pre(fn):
    tp = loadtxt(fn)
    t = tp[:,0]
    y = tp[:,1]
    yres = tp[:,2]

    plt.plot_date(t+_adj_dates, y, 'x', color='lightblue', label='original')
    plt.plot_date(t+_adj_dates, yres, 'x', color='lightgreen', label='residual')

    linsec = read_linsec(fn)

    ch = tcut_ts(t, linsec)
    
    plt.plot_date(t[ch]+_adj_dates, y[ch], 'x', color='blue', label='original')
    plt.plot_date(t[ch]+_adj_dates, yres[ch], 'x', color='green', label='residual')

    plt.grid('on')
    

    
    
