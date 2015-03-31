import viscojapan as vj

site = '_KMN'
#site = 'ULAB'
#site = 'J765'
site = 'J550'
site = 'J162'
##site = 'J619'
##site = 'J401'
##site = 'G031'
site = 'J401'

#for cmpt in 'e', 'n', 'u':
for cmpt in 'enu':
    plt = vj.inv.PredictedTimeSeriesPlotter(
        '../deformation_partition/deformation_partition.h5')

    plt.plot_cumu_disp_decomposition(site, cmpt)
    plt.plt.savefig('{site}-{cmpt}-cumu.pdf'.format(site=site, cmpt=cmpt))
    #plt.plt.show()
    plt.plt.close()

    plt.plot_post_disp_decomposition(site, cmpt)
    plt.plt.savefig('{site}-{cmpt}-post.pdf'.format(site=site, cmpt=cmpt))
    #plt.plt.show()
    plt.plt.close()

    plt = vj.inv.PredictedVelocityTimeSeriesPlotter(
        '../deformation_partition/deformation_partition.h5')
    plt.plot_vel_decomposition(site, cmpt)
    plt.plt.savefig('{site}-{cmpt}-vel.pdf'.format(site=site, cmpt=cmpt))
    #plt.plt.show()
    plt.plt.close()
