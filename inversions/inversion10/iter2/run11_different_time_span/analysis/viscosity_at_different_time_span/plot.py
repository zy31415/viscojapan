import glob

from pylab import plt

import viscojapan as vj

from epochs import epochs_list

files = sorted(glob.glob('../../outs/nepochs_??_nrough_06_naslip_11.h5'))

vises = []
Hes = []
for f in files:
    nth_epochs = int(f.split('_')[-5])
    print(nth_epochs)
    reader = vj.inv.ResultFileReader(f)
    log_vis = reader.get_nlin_par_solved_value('log10(visM)')
    log_He = reader.get_nlin_par_solved_value('log10(He)')
    vis = 10**log_vis
    He = 10**log_He
    
    vises.append(vis)
    Hes.append(He)

max_time = [max(epochs) for epochs in epochs_list]

ax1 = plt.subplot(211)
plt.plot(max_time, vises, 'x-')
plt.grid('on')
plt.ylabel(r'viscosity $(Pa \cdot s)$')
plt.setp(ax1.get_xticklabels(), visible=False)

plt.subplot(212, sharex=ax1)
plt.plot(max_time, Hes, '^-')
plt.ylabel(r'He (km)')
plt.grid('on')
plt.xlabel('days of data used')

plt.savefig('diff_days_span.png')
plt.show()

