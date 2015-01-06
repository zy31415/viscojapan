import viscojapan as vj

#site = '_KMN'
#site = 'ULAB'
site = 'J550'

#for cmpt in 'e', 'n', 'u':
for cmpt in ['e']:
    plt = vj.inv.PredictedTimeSeriesPlotter('../pred_disp/~pred_disp.db')

    plt.plot_cumu_disp(site, cmpt)
    plt.plt.show()
    plt.plt.close()

    plt.plot_post_disp(site, cmpt)
    plt.plt.show()
    plt.plt.close()
