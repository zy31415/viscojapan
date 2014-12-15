import re
from os.path import basename

from numpy import loadtxt, asarray, inf
from pylab import plt

from ..utils import cut_ts
from .linres_file_reader import read_t, read_y, read_yres, read_ysd, \
     read_linsec, read_outlier, read_jumps

_adj_dates = 678577


def outlier_index(t,outliers):
    return [list(t).index(oi) for oi in outliers]

def plot_pre(fn):
    t = read_t(fn)
    y = read_y(fn)
    yres = read_yres(fn)

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
    

    
    
