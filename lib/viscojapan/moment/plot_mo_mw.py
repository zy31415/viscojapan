import matplotlib
from pylab import plt

from .utils import mw_to_mo, mo_to_mw

__author__ = 'zy'

def plot_Mos_Mws(days, Mos=None, Mws=None, ylim = None, yticks=None):
    if Mos is None and Mws is None:
        raise ValueError('Set Mos or Mws.')
    if Mos is not None and Mws is not None:
        raise ValueError("Don't set both.")
    if Mws is not None:
        Mos = mw_to_mo(Mws)

    fig, ax1 = plt.subplots()
    ax1.plot(days, Mos,'-o')
    ax1.set_yscale('log')

    if yticks is not None:
        ax1.set_yticks(yticks)
    ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    if ylim is not None:
        ax1.set_ylim(ylim)

    lim1 = ax1.get_ylim()

    ax1.set_xlabel('days after the mainshock')
    ax1.set_ylabel('Moment(Nm)')
    ax1.grid('on')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Mw')
    ax2.set_ylim(mo_to_mw(lim1))
