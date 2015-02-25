import pickle

import numpy as np
from pylab import plt

import viscojapan as vj
from viscojapan.tsana.post_fit.post import fit_post

site = 'J550'
cmpt = 'e'

ax1 = plt.subplot(2,1,1)

with open('cfs.pkl/%s.pkl'%site, 'rb') as fid:
    cfs = pickle.load(fid)
cf = cfs[0]
f1 = cf.get_subf('EXP1')
f2 = cf.get_subf('EXP2')

days = np.arange(0, 1344) + 55631
y1 = f1(days)
y2 = f2(days)

reader = vj.tsana.ObservationDatatbaseReader(obs_db='../../tsana/db/~observation.db')
t_obs, y_obs = reader.get_post_obs_linres(site,cmpt)

plt.plot_date(t_obs + 55631+vj.adjust_mjd_for_plot_date,
              y_obs,
              'x',
              color='blue', label='obs.')
plt.plot_date(days + vj.adjust_mjd_for_plot_date,
              y1+y2,
              '-',
              lw=3,
              color='red', label='EXP1 + EXP2')
plt.plot_date(days + vj.adjust_mjd_for_plot_date, y1, '-', color=r'green',
              label = 'EXP1')
plt.plot_date(days  + vj.adjust_mjd_for_plot_date, y2, '-', color=r'orange',
              label = 'EXP2')
plt.ylim([0,1])
plt.grid('on')
plt.legend(loc=2, prop={'size':6})

ax2 = plt.subplot(212, sharex=ax1)
pplt = vj.inv.PredictedTimeSeriesPlotter('../../inversions/inversion10/iter2/run7/analysis/pred_disp/~pred_disp.db')
pplt.plot_post_disp_decomposition(site, cmpt)
plt.title('')
plt.ylim([0,1])
plt.savefig('2EXPs_vs_pred_%s-%s.png'%(site, cmpt))
plt.savefig('2EXPs_vs_pred_%s-%s.pdf'%(site, cmpt))
plt.show()
