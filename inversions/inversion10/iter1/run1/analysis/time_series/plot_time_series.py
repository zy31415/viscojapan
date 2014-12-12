import viscojapan as vj

site = 'J550'
cmpt = 'e'

plt = vj.inv.TimeSeriesPlotter('../pred_disp/~pred_disp.db')
plt.plot_linres(site, cmpt)
plt.plt.show()

