from pylab import plt
from matplotlib.font_manager import FontProperties

__author__ = 'zy'
__all__ = ['plot_slip_and_rate_at_subflt']

def plot_slip_and_rate_at_subflt(slip, nth_dip, nth_stk):
    epochs = slip.get_epochs()

    ts_slip = slip.get_cumu_slip_at_subfault(nth_dip, nth_stk)
    ts_rate = slip.get_slip_rate_at_subfault(nth_dip, nth_stk)

    fig, ax1 = plt.subplots()
    ln1 = ax1.plot(epochs, ts_slip, 'r^-', label='Slip')
    ax1.grid('on')
    ax1.set_ylabel('Slip/m')
    ax1.set_xlabel('Days after the mainshock')

    ax2 = ax1. twinx()
    ln2 = ax2.plot(epochs[1:], ts_rate, 'bo-', label='Rate')
    ax2.set_ylabel('Rate/(m/day)')

    fontP = FontProperties()
    fontP.set_size('small')

    lns = ln1 + ln2
    labs = [l.get_label() for l in lns]
    ax2.legend(lns, labs, loc=1,
               prop = fontP,
               bbox_to_anchor=(1.1, 1.05))

