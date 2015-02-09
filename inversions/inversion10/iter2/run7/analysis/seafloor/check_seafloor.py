from pylab import plt
import numpy as np

import viscojapan as vj

bd = .3

for site in '_CHS','_FUK', '_KMN', '_KMS', '_MGI', '_MGW':    
    for cmpt in 'e', 'n', 'u':
        reader = vj.inv.ResultFileReader('../../outs/nrough_06_naslip_11.h5')
        y_pred, t_pred = reader.get_pred_time_series(site, cmpt)
        plt.plot(t_pred,y_pred,'-o')

        tp = np.loadtxt('../../../../../../tsana/sea_floor/cumu_post/%s.original'%site)
        t = tp[:,0]
        if cmpt == 'e':
            nth = 1
        elif cmpt == 'n':
            nth = 2
        elif cmpt == 'u':
            nth = 3
        y = tp[:,nth]
        plt.plot(t,y,'x',color='red')

        y1 = np.amin(list(y_pred)+list(y))
        y2 = np.amax(list(y_pred)+list(y))
        dy = y2 - y1
        y1 -= bd*dy
        y2 += bd*dy
        plt.ylim((y1,y2))

        plt.grid('on')
        plt.xlabel('days after mainshock')
        plt.ylabel('displacement (m)')

        name = vj.sites_db.get_site_true_name(site)
        plt.title('%s-%s'%(name, cmpt))
        
        plt.savefig('plots_seafloor/%s-%s.pdf'%(site,cmpt))
        #plt.show()
        plt.close()
