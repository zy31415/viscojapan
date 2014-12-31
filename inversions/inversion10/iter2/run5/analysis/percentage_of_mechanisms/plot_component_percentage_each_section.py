import sqlite3

import numpy as np
from pylab import plt
import matplotlib.patches as mpatches

db_file = '../pred_disp/~pred_disp.db'

def get_data_matrix(tb):
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        tp = c.execute('select e,n,u from %s order by day, site;'%tb).\
             fetchall()
        num_sites = c.execute('select count(distinct site) from %s;'%tb).\
                     fetchall()[0][0]
        epochs = c.execute('select distinct day from %s;'%tb).\
                     fetchall()
    epochs = [ii[0] for ii in epochs]
    num_epochs = len(epochs)

    arr = np.asarray(tp).flatten()
    arr = arr.reshape([num_epochs, num_sites*3])

    return arr.T, epochs

Rco, epochs = get_data_matrix('tb_R_co')
Raslip, _ = get_data_matrix('tb_R_aslip')
Easlip, _ = get_data_matrix('view_E_aslip')

Rco = np.diff(Rco, axis=1)
Raslip = np.diff(Raslip, axis=1)
Easlip = np.diff(Easlip, axis=1)


total = Rco + Raslip + Easlip

ch1 = (Easlip*total>0)
ch2 = (Rco*total>0)
ch3 = (Raslip*total>0)
mask = (ch1 & ch2 & ch3)


def compute_percentage(part, total):
    percentage = abs(part)/abs(total)
    percentage[~mask] = np.nan
    return percentage

percentage_Easlip = compute_percentage(Easlip, total)
percentage_Rco = compute_percentage(Rco, total)
percentage_Raslip = compute_percentage(Raslip, total)

mean_percentage_Easlip = np.nanmean(percentage_Easlip, axis=0)
mean_percentage_Rco = np.nanmean(percentage_Rco, axis=0)
mean_percentage_Raslip = np.nanmean(percentage_Raslip, axis=0)

total_percentage = mean_percentage_Easlip + mean_percentage_Rco +mean_percentage_Raslip

################################

ts = []
for t1, t2 in zip(epochs[0:-1],epochs[1:]):
    ts += [t1,t2]

ys1 = []
for yi in mean_percentage_Easlip:
    ys1 += [yi,yi]

plt.fill_between(ts, ys1, np.zeros_like(ys1), color='blue')

ys2 = []
for yi in mean_percentage_Rco:
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
