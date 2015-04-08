from pylab import plt
import numpy as np

import viscojapan as vj

reader = vj.EpochalSitesFileReader('cumu_post_with_seafloor.h5')

site  = '_KMN'
cmpt = 'u'
t = reader.get_epochs()
y = reader.get_time_series_at_site(site,cmpt)

tp = np.loadtxt('../../../../tsana/sea_floor/postseismic/fit_2EXPs/cumu_post_displacement/%s.cumu'%site)

plt.plot(t,y, color='black')
if cmpt =='e':
    nth = 1
elif cmpt == 'n':
    nth = 2
elif cmpt == 'u':
    nth = 3
    
plt.plot(tp[:,0], tp[:,nth], color='red')
plt.show()
