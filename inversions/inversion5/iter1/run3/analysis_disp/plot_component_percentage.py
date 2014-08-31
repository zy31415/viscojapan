import numpy as np
from pylab import plt

from epochs_log import epochs

def load_array(fn):
    tp = np.loadtxt(fn, '4a,1a,20f')
    return np.asarray([ii[2] for ii in tp])

percentage_elastic = load_array('disp_cmpts/percentage_elastic')
percentage_Rco = load_array('disp_cmpts/percentage_Rco')
percentage_Raslip = load_array('disp_cmpts/percentage_Raslip')

mean_elastic = np.nanmean(percentage_elastic, axis=0)
mean_Rco = np.nanmean(percentage_Rco, axis=0)
mean_Raslip = np.nanmean(percentage_Raslip, axis=0)


plt.plot(epochs[1:], mean_elastic,'o-', label=r'$E^{\bf{aslip}}$')
plt.plot(epochs[1:], mean_Rco,'^-', label = r'$R^{\bf{co}}$')
plt.plot(epochs[1:], mean_Raslip,'v-', label = r'$R^{\bf{aslip}}$')

plt.grid('on')
plt.legend()
plt.xlabel('days after the mainshock')
plt.ylabel('percentage')
plt.savefig('plots/percentage_components.png')
plt.savefig('plots/percentage_components.pdf')
plt.show()
