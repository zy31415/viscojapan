import numpy as np
from pylab import plt

site = 'J550'
cmpt = 'e'
tp = np.loadtxt('../../pre_fit/linres/%s.%s.lres'%(site,cmpt))

t = tp[:,0]
y = tp[:,1]
yres = tp[:,2]

plt.plot(t,yres,'x')
plt.show()
