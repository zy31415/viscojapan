import viscojapan as vj

site = 'J550'

#for cmpt in 'e', 'n', 'u':
for cmpt in ['e']:
    plt = vj.inv.PredictedTimeSeriesPlotter('../pred_disp/~pred_disp.db')

##    plt.plot_cumu_disp(site, cmpt,
##                       if_plot_added=True
##                       )
##    plt.plt.show()
##    plt.plt.close()

    plt.plot_post_disp(site, cmpt,
                       if_plot_added=True
                       )
    plt.plt.show()
    plt.plt.close()
