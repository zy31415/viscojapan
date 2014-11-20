import glob

import h5py
from pylab import plt
from numpy import log10, amin, amax
import matplotlib

from .collect_from_result_files import collect_from_result_files

__all__ = ['plot_L_curve']

def plot_L_curve(files,
                 nlin_pars = ['log10_He_','log10_visM_','rake'],
                 nlin_pars_ylabels = [r'$log_{10}(He)$',
                                      r'$log_{10}(visM)$',
                                      'rake'],
                 ):
    nreses = collect_from_result_files(files, 'residual_norm_weighted')
    nroughs = collect_from_result_files(files, 'roughening_norm')
    num_subplots = 1 + len(nlin_pars)

    x1 = amin(nreses)
    x2 = amax(nreses)
    dx = x2 - x1
    xlim = (x1-dx*0.02, x2+dx*0.2)
    xticks = range(int(x1), int(x2),5)

    plt.subplot(num_subplots,1,1)
    plt.loglog(nreses, nroughs,'o-')
    plt.xlim(xlim)
    plt.gca().set_xticks(xticks)
    plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    plt.ylabel('roughening')
    plt.xlabel('Residual Norm')
    plt.grid('on')

    nth = 2
    for par, par_label in zip(nlin_pars, nlin_pars_ylabels):
        y = collect_from_result_files(files, par)
        plt.subplot(num_subplots,1,nth)
        plt.semilogx(nreses, y,'o-')
        plt.xlim(xlim)
        plt.gca().set_xticks(xticks)
        plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        plt.ylabel(par_label)
        plt.xlabel('Residual Norm')
        plt.grid('on')
        nth += 1
