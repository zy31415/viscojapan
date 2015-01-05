from datetime import date

import numpy as np
from pylab import plt

import viscojapan as vj

site = 'J550'
cmpt = 'e'

tp = np.loadtxt('../../tsana/pre_fit/linres/{site}.{cmpt}.lres'.\
           format(site=site, cmpt=cmpt))

days = tp[:,0]
yres = tp[:,2]

plt.plot_date(days + vj.adjust_mjd_for_plot_date, yres, 'x')
plt.grid('on')

plt.axvline(date(2011,3,11),color='r', ls='--')

plt.ylim([-1, 7])
plt.xlim((date(2010,1,1), date(2015,1,1)))

plt.gcf().autofmt_xdate()

plt.ylabel('m')
plt.title('%s - %s'%(site, cmpt))
plt.savefig('%s_%s.pdf'%(site, cmpt))
plt.show()
