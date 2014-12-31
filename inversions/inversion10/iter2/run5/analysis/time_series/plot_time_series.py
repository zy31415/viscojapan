import viscojapan as vj

site = 'J333'

#for cmpt in 'e', 'n', 'u':
for cmpt in ['u']:
    plt = vj.inv.PredictedTimeSeriesPlotter('../pred_disp/~pred_disp.db')

    plt.plot_cumu_disp(site, cmpt, if_ylim=False)
    plt.plt.show()
    plt.plt.close()

    plt.plot_post_disp(site, cmpt, if_ylim=False)
    plt.plt.show()
    plt.plt.close()
