import viscojapan as vj

site = '_MGI'

for cmpt in 'e', 'n', 'u':
    plt = vj.inv.PredictedTimeSeriesPlotter('../pred_disp/~pred_disp.db')

    plt.plot_cumu_disp(site, cmpt, if_ylim=False)
    plt.plt.show()
    plt.plt.close()

    plt.plot_post_disp(site, cmpt, if_ylim=False)
    plt.plt.show()
    plt.plt.close()
