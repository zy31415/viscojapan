import viscojapan as vj

site = '_FUK'
cmpt = 'e'

plt = vj.inv.TimeSeriesPlotter('../pred_disp/~pred_disp.db')

plt.plot_cumu_obs_linres(site, cmpt)
plt.plot_cumu_disp_pred(site, cmpt)

plt.plot_post_disp_pred(site,cmpt)
plt.plot_post_obs_linres(site,cmpt)

plt.plt.show()

