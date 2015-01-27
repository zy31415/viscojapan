import numpy as np
from pylab import plt

__all__ = ['SubFaultSlipHistoryPlotter']

class SubFaultSlipHistoryPlotter(object):
    def __init__(self,
                 slip,
                 ):
        self.slip = slip
        
    def plot(self, output_file,
             if_x_log=False,
             xlim=[0, 1344],
             ylim = [0,100],
             yticks = [20, 40, 60],
             xticks = [1, 10, 100, 1000],
             xticklabels = [r'$10^0$', r'$10^1$', r'$10^2$', r'$10^3$'],
             rotation = 45,
             fontsize = 10,
             ):
        slip = self.slip.get_3d_cumu_slip()
        num_subflts_strike = slip.shape[2]
        num_subflts_dip = slip.shape[1]        
        
        epochs = self.slip.epochs

        fig, axes = plt.subplots(num_subflts_dip,
                                 num_subflts_strike,
                                 sharex=True, sharey=True)
        for ii in range(num_subflts_dip):
            for jj in range(num_subflts_strike):
                ax = axes[ii][jj]
                slip_subflt = slip[:,ii,jj]
                plt.sca(ax)
                plt.fill_between(x=epochs, y1=slip_subflt, y2=0, color='r')
                if if_x_log:
                    ax.set_xscale('log')                    
                plt.xlim(xlim)
                plt.ylim(ylim)
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
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticklabels, rotation=rotation, fontsize=fontsize)
            plt.xlabel('day')

        for ax in axes[0,1::2]:
            plt.sca(ax)
            plt.tick_params(axis='x',which='major',
                                bottom='off', top='on', left='off', right='off',
                                labelbottom='off', labeltop='on', labelleft='off', labelright='off')
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticklabels, rotation=rotation, fontsize=fontsize)
            plt.xlabel('day')

        for ax in axes[::2,0]:
            plt.sca(ax)
            plt.tick_params(axis='y',which='major',
                                bottom='off', top='off', left='on', right='off',
                                labelbottom='off', labeltop='off', labelleft='on', labelright='off')
            ax.set_yticks(yticks)
            #ax.set_yticklabels(range(0,100,20))
            for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(10)
                tick.label.set_rotation('horizontal')
            plt.ylabel('slip/m')

        for ax in axes[::2,-1]:
            plt.sca(ax)
            plt.tick_params(axis='y',which='major',
                                bottom='off', top='off', left='off', right='on',
                                labelbottom='off', labeltop='off', labelleft='off', labelright='on')
            ax.set_yticks(yticks)
            #ax.set_yticklabels(range(0,100,20))
            for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(10)
                tick.label.set_rotation('horizontal')
            plt.ylabel('slip/m')
            ax.yaxis.set_label_position("right")

        fig.set_size_inches(33,10)
        plt.savefig(output_file)
        plt.close()

        


