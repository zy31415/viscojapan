import pickle

import numpy as np
from pylab import plt

import viscojapan as vj
from viscojapan.tsana.post_fit.post import fit_post

site = 'J550'
cmpt = 'e'
ylim = (-0.1, 1)

pplt = vj.inv.PredictedTimeSeriesPlotter(
    partition_file = 'deformation_partition.h5',
    result_file = 'nrough_06_naslip_11.h5'
    )

pplt.plot_post_disp_decomposition(site, cmpt,
                    marker_for_obs='.')
plt.ylim(ylim)

def ajust_xaxis_tick_labels(ax):
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(8)
        # specify integer or one of preset strings, e.g.
        #tick.label.set_fontsize('x-small')
        tick.label.set_rotation('vertical')

ajust_xaxis_tick_labels(plt.gca())

plt.savefig('model_prediction_%s-%s.png'%(site, cmpt))
plt.savefig('model_prediction_%s-%s.pdf'%(site, cmpt))
plt.show()
