import viscojapan as vj

site = 'J120'
cmpt = 'e'

plt = vj.inv.TimeSeriesPlotter('../pred_disp/~pred_disp.db')
plt.plot_linres(site, cmpt)
plt.plot_cumu_disp_pred(site, cmpt)
plt.plot_post_disp_pred(site,cmpt)
plt.plt.show()

