import numpy as np
from pylab import plt

from .result_file_reader import ResultFileReader

__all__ = ['FaultSlipPlotter']

class FaultSlipPlotter(object):
    def __init__(self,
                 result_file,
                 fault_file):
        self.result_file = result_file
        self.reader_result_file = ResultFileReader(
            self.result_file,
            fault_file)
        
    def plot(self, output_file):
        slip = self.reader_result_file.get_3d_total_slip()
        num_subflts_strike = slip.shape[2]
        num_subflts_dip = slip.shape[1]        
        
        epochs = self.reader_result_file.epochs        

        fig, axes = plt.subplots(num_subflts_dip,
                                 num_subflts_strike,
                                 sharex=True, sharey=True)
        for ii in range(num_subflts_dip):
            for jj in range(num_subflts_strike):
                ax = axes[ii][jj]
                slip_subflt = slip[:,ii,jj][0:-1]
                plt.sca(ax)
                plt.fill_between(x=epochs, y1=slip_subflt, y2=0, color='r')
                ax.set_xscale('log')
                plt.xlim([0.1, 300])
                plt.ylim([0,100])
                plt.grid('on')
                plt.box('on')

                plt.tick_params(axis='both',which='both',
                                bottom='off', top='off', left='off', right='off',
                                labelbottom='off', labeltop='off', labelleft='off', labelright='off')
               
        fig.subplots_adjust(hspace=0, wspace=0)

        for ax in axes[-1,::2]:
            plt.sca(ax)
            plt.tick_params(axis='x',which='major',
                                bottom='on', top='off', left='off', right='off',
                                labelbottom='on', labeltop='off', labelleft='off', labelright='off')
            ax.set_xticks([1, 10, 100, 1000])
            ax.set_xticklabels([r'$10^0$', r'$10^1$', r'$10^2$', r'$10^3$'])
            for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(10)
                tick.label.set_rotation('horizontal')
            plt.xlabel('day')

        for ax in axes[0,1::2]:
            plt.sca(ax)
            plt.tick_params(axis='x',which='major',
                                bottom='off', top='on', left='off', right='off',
                                labelbottom='off', labeltop='on', labelleft='off', labelright='off')
            ax.set_xticks([1, 10, 100, 1000])
            ax.set_xticklabels([r'$10^0$', r'$10^1$', r'$10^2$', r'$10^3$'])
            for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(10)
                tick.label.set_rotation('horizontal')
            plt.xlabel('day')

        for ax in axes[::2,0]:
            plt.sca(ax)
            plt.tick_params(axis='y',which='major',
                                bottom='off', top='off', left='on', right='off',
                                labelbottom='off', labeltop='off', labelleft='on', labelright='off')
            ax.set_yticklabels(range(0,100,20))
            for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(10)
                tick.label.set_rotation('horizontal')
            plt.ylabel('slip/m')

        for ax in axes[::2,-1]:
            plt.sca(ax)
            plt.tick_params(axis='y',which='major',
                                bottom='off', top='off', left='off', right='on',
                                labelbottom='off', labeltop='off', labelleft='off', labelright='on')
            ax.set_yticklabels(range(0,100,20))
            for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(10)
                tick.label.set_rotation('horizontal')
            plt.ylabel('slip/m')
            ax.yaxis.set_label_position("right")

        fig.set_size_inches(33,10)
        plt.savefig(output_file)
        plt.close()

        


