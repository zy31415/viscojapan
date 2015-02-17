import pickle

import numpy as np
from pylab import plt

import viscojapan as vj
from viscojapan.tsana.post_fit.post import fit_post

site = 'J550'
cmpt = 'e'
ylim = (-0.1, 1)

##############
ax1 = plt.subplot(221)
with open('%s_EXP.pkl'%site, 'rb') as fid:
    cfs = pickle.load(fid)
cf = cfs[0]
f1 = cf.get_subf('EXP')

days = np.arange(0, 1344) + 55631
y1 = f1(days)

ch = cf.data.t > 55631
t_obs = cf.data.t[ch]
y_obs = cf.data.y0[ch] - cf._func.get_subf('TOHOKU').jump

ax1.plot_date(t_obs +vj.adjust_mjd_for_plot_date,
              y_obs, '.',
              color='blue', label='obs.')
ax1.plot_date(days + vj.adjust_mjd_for_plot_date, y1, '-',
              lw=2, color='red', label='EXP')

ch = cf.data.t > 55631
ax1.plot_date(cf.data.t[ch] + vj.adjust_mjd_for_plot_date, cf.residual()[ch], '.',
              color=r'blue',
              label = 'residual',
              markersize=1)

ax1.set_ylabel('m')
ax1.set_ylim(ylim)
ax1.grid('on')
ax1.legend(loc=2, prop={'size':6})
ax1.set_title('(a)')

########################
ax2 = plt.subplot(222, sharey=ax1)

with open('%s_2EXPs.pkl'%site, 'rb') as fid:
    cfs = pickle.load(fid)
cf = cfs[0]
f1 = cf.get_subf('EXP1')
f2 = cf.get_subf('EXP2')

days = np.arange(0, 1344) + 55631
y1 = f1(days)
y2 = f2(days)

ch = cf.data.t > 55631
t_obs = cf.data.t[ch]
y_obs = cf.data.y0[ch] - cf._func.get_subf('TOHOKU').jump

ax2.plot_date(t_obs + vj.adjust_mjd_for_plot_date,
              y_obs, '.', color='blue', label='obs.')
ax2.plot_date(days + vj.adjust_mjd_for_plot_date,
              y1+y2, '-', lw=2,
              color='red', label='EXP1 + EXP2')
ax2.plot_date(days + vj.adjust_mjd_for_plot_date, y1, '-', color=r'green',
              label = 'EXP1')
ax2.plot_date(days  + vj.adjust_mjd_for_plot_date, y2, '-', color=r'orange',
              label = 'EXP2')

ch = cf.data.t > 55631
ax2.plot_date(cf.data.t[ch] + vj.adjust_mjd_for_plot_date, cf.residual()[ch], '.',
              color=r'blue',
              label = 'residual',
              markersize=1)

ax2.set_ylim(ylim)
ax2.grid('on')
ax2.legend(loc=2, prop={'size':6})
ax2.set_title('(b)')

############# 
ax3 = plt.subplot(224, sharex=ax2)

pplt = vj.inv.PredictedTimeSeriesPlotter(
    partition_file = 'partition.h5',
    result_file = 'nrough_05_naslip_11.h5'
    )
pplt.plot_post_disp(site, cmpt,
                    marker_for_obs='.')
plt.title('')
plt.ylim(ylim)
ax3.set_title('(c)')

def ajust_xaxis_tick_labels(ax):
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(8)
        # specify integer or one of preset strings, e.g.
        #tick.label.set_fontsize('x-small')
        tick.label.set_rotation('vertical')

ajust_xaxis_tick_labels(ax3)
plt.setp(ax1.get_xticklabels(), visible=True)
ajust_xaxis_tick_labels(ax1)


plt.savefig('2EXPs_EXP_pred_%s-%s.png'%(site, cmpt))
plt.savefig('2EXPs_EXP_pred_%s-%s.pdf'%(site, cmpt))
plt.show()
