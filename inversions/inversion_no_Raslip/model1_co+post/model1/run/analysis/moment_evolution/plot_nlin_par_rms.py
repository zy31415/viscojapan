import glob

import h5py
from pylab import plt
from numpy import log10, amin, amax
import matplotlib

import viscojapan as vj

nres =[]
visMs = []
Hes = []
rakes = []
nroughs = []

files = sorted(glob.glob('outs/*.h5'))

nres = vj.collect_from_result_files(files, 'residual_norm_weighted')
log10_He_ = vj.collect_from_result_files(files, 'log10_He_')
log10_visM_ = vj.collect_from_result_files(files, 'log10_visM_')
rakes = vj.collect_from_result_files(files, 'rake')
nroughs = vj.collect_from_result_files(files, 'roughening_norm')


x1 = amin(nres)
x2 = amax(nres)
dx = x2 - x1
xlim = (x1-dx*0.02, x2+dx*0.2)
xticks = range(int(x1), int(x2),5)

plt.subplot(411)    
plt.semilogx(nres, log10_visM_,'o')
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.axhline(18.8, color='red')
plt.grid('on')
plt.ylabel('log10(visM/(Pa.s))')

plt.subplot(412)    
plt.semilogx(nres, log10_He_,'o')
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
#plt.axhline(40, color='red')
plt.grid('on')
plt.ylabel('He/km')

plt.subplot(413)    
plt.semilogx(nres, rakes,'o')
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.axhline(83, color='red')
plt.ylabel('rake')
plt.grid('on')

plt.subplot(414)
vj.plots.plot_L(nres, nroughs)
plt.xlim(xlim)
plt.gca().set_xticks(xticks)
plt.gca().get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.ylabel('roughening')
plt.xlabel('Residual Norm')
plt.grid('on')

plt.savefig('plots/nlin_par_curve_rms.png')
plt.show()
