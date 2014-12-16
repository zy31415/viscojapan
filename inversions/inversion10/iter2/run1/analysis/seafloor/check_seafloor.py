from pylab import plt
import numpy as np

import viscojapan as vj

for site in '_FUK', '_KMN', '_KMS', '_MGI', '_MGW':
    for cmpt in 'e', 'n', 'u':
        reader = vj.inv.ResultFileReader('../../outs/nco_06_naslip_10.h5')
        y_pred, t_pred = reader.get_pred_time_series(site, cmpt)
        plt.plot(t_pred,y_pred)

        tp = np.loadtxt('../../../../../../tsana/sea_floor/cumu_post/%s.original'%site)
        t = tp[:,0]
        if cmpt == 'e':
            nth = 1
        elif cmpt == 'n':
            nth = 2
        elif cmpt == 'u':
            nth = 3
        y = tp[:,nth]
        plt.plot(t,y,'x')

        y1 = np.amin(y_pred)
        y2 = np.amax(y_pred)
        dy = y2 - y1
        y1 -= .2*dy
        y2 += .2*dy
        plt.ylim((y1,y2))

        plt.title('%s-%s'%(site, cmpt))
        
        plt.savefig('plots_seafloor/%s.%s.png'%(site,cmpt))
        #plt.show()
        plt.close()
