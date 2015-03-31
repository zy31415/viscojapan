import numpy as np
from pylab import plt
from matplotlib import gridspec

__author__ = 'zy'

__all__ = ['TimeSeriesAndResidualPlotter']

def ajust_xaxis_tick_labels(ax):
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(8)
        # specify integer or one of preset strings, e.g.
        #tick.label.set_fontsize('x-small')
        tick.label.set_rotation('vertical')

class TimeSeriesAndResidualPlotter(object):
    def __init__(self,
                 ylim1 = [-0.1, 1],
                 ylim2 = [-0.06, 0.06]
                 ):
        self.ylim1 = ylim1
        self.ylim2 = ylim2

        gs = gridspec.GridSpec(2, 1,
                       height_ratios=[4,1],
                       hspace = 0.02
                       )
        self._init_plot_axis_1(gs)
        self._init_plot_axis_2(gs)

        self._lns = []

    def _init_plot_axis_1(self, gs):
        ax1 = plt.subplot(gs[0])

        ax1.grid('on')
        ax1.set_ylabel('meter')
        ax1.set_ylim(self.ylim1)

        #ax1.set_title('(a)')
        #ax1.spines['bottom'].set_visible(False)
        ax1.xaxis.tick_top()
        ax1.axhline(0,ls='..', color='red')

        plt.setp(ax1.get_xticklabels(), visible=False)
        ax1.axhline(0,ls='-.', color='red')
        self.ax1 = ax1

    def _init_plot_axis_2(self, gs):
        ax2 = plt.subplot(gs[1], sharex=self.ax1)
        ax2.axhline(0,ls='-.', color='red')
        ax2.grid('on')
        #ax2.spines['top'].set_visible(False)
        ax2.xaxis.tick_bottom()
        ax2.set_ylim(self.ylim2)
        ajust_xaxis_tick_labels(ax2)
        ax2.set_yticks(np.arange(-0.06,0.061,0.03))
        self.ax2 = ax2

    def plot_on_time_series_axis(self,t,y,*args, **kwargs):
        ln = self.ax1.plot_date(t,y,*args, **kwargs)
        self._lns += ln

    def plot_on_residual_axis(self,t,y,*args, **kwargs):
        ln = self.ax2.plot_date(t,y,*args, **kwargs)
        self._lns += ln

    def legend(self):
        labs = [l.get_label() for l in self._lns]
        self.ax1.legend(self._lns, labs, loc=2, prop={'size':10})