import re

import numpy as np
from pylab import plt

site = 'J940'
cmpt = 'u'

# plot time series:
tp = np.loadtxt('/home/zy/workspace/viscojapan/tsana/pre_fit/linres/%s.%s.lres'%\
           (site, cmpt))

t = tp[:,0] - 55631
y = tp[:,2]
plt.plot(t,y,'x')

# plot prediction
fn = 'disp_cmpts/total'
with open(fn,'rt') as fid:
    res = re.findall('^%s.*%s.*'%(site,cmpt), fid.read(),re.M)[0]

with open(fn,'rt') as fid:
    ln = fid.readline()
    t = np.asarray(ln.split()[4:], int)

y = np.asarray(res.split()[2:], float)
plt.plot(t,y,'red',lw=2)


plt.grid('on')
plt.xlim([-20,1200])
#plt.ylim([-0.01, 0.01])
plt.show()
