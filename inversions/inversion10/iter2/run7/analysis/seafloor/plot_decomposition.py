import viscojapan as vj

site = '_MGI'

for site in '_CHS', '_FUK', '_KMN', '_KMS', '_MGI', '_MGW': 
    for cmpt in 'e', 'n', 'u':
        plt = vj.inv.PredictedTimeSeriesPlotter('../pred_disp/~pred_disp.db')

    ##    plt.plot_cumu_disp(site, cmpt, if_ylim=False)
    ##    plt.plt.show()
    ##    plt.plt.close()

        plt.plot_post_disp(site, cmpt, if_ylim=False)
        name = vj.sites_db.get_site_true_name(site)
        plt.plt.title('%s - %s'%(name, cmpt))
        #plt.plt.show()
        plt.plt.savefig('plots_seafloor/%s-%s-decmp.pdf'%(site, cmpt))
        plt.plt.close()
