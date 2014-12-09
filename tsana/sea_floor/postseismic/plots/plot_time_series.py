import numpy as np
from pylab import plt

import date_conversion as dc

site = 'KAMS'

def plot(site):
    tp = np.loadtxt('../post_offsets/%s.post'%site)

    t = dc.asmjd([ii[0] for ii in tp]) + dc.adjust_mjd_for_plot_date
    e = [ii[1] for ii in tp]
    n = [ii[2] for ii in tp]
    u = [ii[3] for ii in tp]

    plt.plot_date(t,e,'x-', label = 'eastings')
    plt.plot(t,n,'x-', label = 'northings')
    plt.plot(t,u,'x-', label = 'upings')
    plt.gcf().autofmt_xdate()
    plt.legend(loc=0)
    plt.title(site)
    plt.savefig('%s.png'%site)
    #plt.show()
    plt.close()


for site in 'KAMS','FUKU','KAMN','KAMS','MYGI','MYGW','CHOS':
    plot(site)
