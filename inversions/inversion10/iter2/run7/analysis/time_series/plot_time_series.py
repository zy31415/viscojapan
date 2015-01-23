import viscojapan as vj

site = '_KMN'
#site = 'ULAB'
#site = 'J765'
site = 'J550'
site = 'J166'

#for cmpt in 'e', 'n', 'u':
for cmpt in 'en':
    plt = vj.inv.PredictedTimeSeriesPlotter('../pred_disp/~pred_disp.db')

    plt.plot_cumu_disp(site, cmpt)
    plt.plt.savefig('{site}-{cmpt}-cumu.pdf'.format(site=site, cmpt=cmpt))
    #plt.plt.show()
    plt.plt.close()

    plt.plot_post_disp(site, cmpt)
    plt.plt.savefig('{site}-{cmpt}.pdf'.format(site=site, cmpt=cmpt))
    #plt.plt.show()
    plt.plt.close()
