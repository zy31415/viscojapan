import numpy as np
from pylab import plt
import matplotlib.patches as mpatches

from epochs_log import epochs

def load_array(fn):
    tp = np.loadtxt(fn, '4a,1a,19f')
    return np.asarray([ii[2] for ii in tp])

percentage_elastic = load_array('disp_cmpts/percentage_elastic_each_section')
percentage_Rco = load_array('disp_cmpts/percentage_Rco_each_section')
percentage_Raslip = load_array('disp_cmpts/percentage_Raslip_each_section')

mean_elastic = np.nanmean(percentage_elastic, axis=0)
mean_Rco = np.nanmean(percentage_Rco, axis=0)
mean_Raslip = np.nanmean(percentage_Raslip, axis=0)

ts = []
for t1, t2 in zip(epochs[1:-1],epochs[2:]):
    ts += [t1,t2]

ys1 = []
for yi in mean_elastic:
    ys1 += [yi,yi]

plt.fill_between(ts, ys1, np.zeros_like(ys1), color='blue')

ys2 = []
for yi in mean_Rco:
    ys2 += [1-yi, 1-yi]
plt.fill_between(ts, ys2, np.ones_like(ys2), color='green')

obj = plt.fill_between(ts, ys1, ys2, color='red')

plt.grid('off')

label_patch1 = mpatches.Patch(color='green')
label_patch2 = mpatches.Patch(color='red')
label_patch3 = mpatches.Patch(color='blue')
plt.legend([label_patch1, label_patch2, label_patch3],
           [r'$R^{\bf{co}}$', r'$R^{\bf{aslip}}$',r'$E^{\bf{aslip}}$'],
           bbox_to_anchor=(1.13,1.01))

#plt.gca().set_xscale('log')

for epoch in epochs:
    plt.axvline(epoch,ls='--',color='gray')

plt.xlabel('days after the mainshock')
plt.ylabel('percentage')
plt.savefig('plots/percentage_components_each_section.png')
plt.savefig('plots/percentage_components_each_section.pdf')
plt.show()
