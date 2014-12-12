import numpy as np
from pylab import plt

import viscojapan as vj

site = '_FUK'
cmpt = 'e'

tp = np.loadtxt('../../../../../../tsana/pre_fit/linres/%s.%s.lres'%(site, cmpt))
t = tp[:,0]
ch = (t>=55631)
y_obs = tp[:,2]
plt.plot(t[ch] - 55631, y_obs[ch],'x', color='green')

reader = vj.inv.ResultFileReader('../../outs/nco_06_naslip_10.h5')
y, t = reader.get_pred_time_series(site, cmpt)
plt.plot(t, y, color='red', label='pred', lw=4)
    
tp = np.loadtxt('../../../../../../tsana/post_fit/cumu_post_displacement/%s.cumu'%site)
t = tp[:,0]
if cmpt == 'e':
    y_obs = tp[:,1]
elif cmpt == 'n':
    y_obs = tp[:,2]
elif cmpt == 'u':
    y_obs = tp[:,3]

plt.plot(t, y_obs, color='blue', label='ts model')



plt.legend()
plt.show()

