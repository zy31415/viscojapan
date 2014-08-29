import re

import numpy as np
from pylab import plt

from epochs_log import epochs

site = 'J711'
cmpt = 'e'

def read_results_file(site, cmpt, file):
    with open(file,'rt') as fid:
        tp = re.findall('^%s %s.*'%(site,cmpt),fid.read(),re.M)[0].split()
        y = np.asarray([ii for ii in tp[2:]], float)
        return y   

def read_observation(site, cmpt):
    tp = np.loadtxt('/home/zy/workspace/viscojapan/tsana/post_fit/cumu_post_displacement/%s.cumu'\
                %(site))
    t = tp[:,0]
    y_obs_e = tp[:,1]
    y_obs_n = tp[:,2]
    y_obs_u = tp[:,3]
    if cmpt == 'e':
        return t, y_obs_e
    if cmpt == 'n':
        return t, y_obs_n
    if cmpt == 'u':
        return t, y_obs_u
    

y_total = read_results_file(site, cmpt, 'total')
y_elastic = read_results_file(site, cmpt, 'elastic')
y_Rco = read_results_file(site, cmpt, 'Rco')
y_Raslip = read_results_file(site, cmpt, 'Raslip')
_y = y_elastic + y_Rco +  y_Raslip

for y, label in zip((y_total, y_elastic, y_Rco, y_Raslip, _y),
                    ('total', 'elastic', r'$R_{\bf{co}}$', r'$R_{\bf{aslip}}$',
                     'y_')):
    #plt.semilogx(epochs,y,'o-', label=label)
    plt.plot(epochs,y,'o-', label=label)

t_obs, y_obs = read_observation(site, cmpt)
plt.plot(t_obs, y_obs,'--', label='obs')

plt.grid('on')
plt.legend()
plt.show()

