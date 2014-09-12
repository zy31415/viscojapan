import numpy as np
from pylab import plt

import viscojapan as vj

reader = vj.ReadEarthModelFile('earth.modelBURG-SUM_40km')

dep = np.arange(2.01,100)
shear = reader.get_shear_modulus(dep)/1e9

tp = np.loadtxt('prem.model')
shear_prem = tp[:,5]
dep_prem = 6371-tp[:,0]

plt.plot(dep, shear)
plt.plot(dep_prem, shear_prem)
plt.xlim([0,150])
plt.show()


