import viscojapan as vj

site = '_KMN'
#site = 'ULAB'
#site = 'J765'
site = 'J550'
site = 'J166'

#for cmpt in 'e', 'n', 'u':
for cmpt in 'en':
    plt = vj.inv.PredictedTimeSeriesPlotter(
        '../deformation_partition/deformation_partition.h5')

    plt.plot_cumu_disp_decomposition(site, cmpt)
    plt.plt.savefig('{site}-{cmpt}-cumu.png'.format(site=site, cmpt=cmpt))
    plt.plt.show()
    plt.plt.close()

    plt.plot_post_disp_decomposition(site, cmpt)
    plt.plt.savefig('{site}-{cmpt}.png'.format(site=site, cmpt=cmpt))
    plt.plt.show()
    plt.plt.close()
