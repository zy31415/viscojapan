import re

import numpy as np
from pylab import plt

from epochs_log import epochs

import argparse

parser = argparse.ArgumentParser(description='Plot time series.')
parser.add_argument('site', nargs=1, help='site')
parser.add_argument('-p', action='store_true', help='If show the plot.')
parser.add_argument('-o', nargs='*', default=False, help='Output a file.')

args = parser.parse_args()

site = args.site[0]

def read_results_file(site, cmpt, file):
    with open(file,'rt') as fid:
        tp = re.findall('^%s %s.*'%(site,cmpt),fid.read(),re.M)[0].split()
        y = np.asarray([ii for ii in tp[2:]], float)
        return y   

def read_observation(site):
    tp = np.loadtxt('/home/zy/workspace/viscojapan/tsana/post_fit/cumu_post_displacement/%s.cumu'\
                %(site))
    t = tp[:,0]
    y_obs_e = tp[:,1]
    y_obs_n = tp[:,2]
    y_obs_u = tp[:,3]
    return t, y_obs_e, y_obs_n, y_obs_u

def plot_predicated_components(cmpt):    
    y_total = read_results_file(site, cmpt, 'disp_cmpts/total')
    y_elastic = read_results_file(site, cmpt, 'disp_cmpts/elastic')
    y_Rco = read_results_file(site, cmpt, 'disp_cmpts/Rco')
    y_Raslip = read_results_file(site, cmpt, 'disp_cmpts/Raslip')
    _y = y_elastic + y_Rco +  y_Raslip

    for y, label in zip((y_total, y_elastic, y_Rco, y_Raslip, _y),
                        ('total', 'elastic', r'$R_{\bf{co}}$', r'$R_{\bf{aslip}}$',
                         'total_')):
        #plt.semilogx(epochs,y,'o-', label=label)
        plt.plot(epochs,y,'o-', label=label)

t_obs, e_obs, n_obs, u_obs = read_observation(site)


def set_axis(cmpt):
    plt.grid('on')
    plt.ylabel('%s/m'%cmpt)
    plt.xlim([0,1150])

f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

plt.sca(ax1)
plt.title('%s'%(site))
plot_predicated_components('e')
plt.plot(t_obs, e_obs, '--', label='obs', color='black')
set_axis('east')
plt.legend(prop={'size':8}, bbox_to_anchor=(1.12,1.01))

plt.sca(ax2)
plot_predicated_components('n')
plt.plot(t_obs, n_obs,'--', label='obs', color='black')
set_axis('north')

plt.sca(ax3)
plot_predicated_components('u')
plt.plot(t_obs, u_obs,'--', label='obs', color='black')
plt.xlabel('days after the mainshock')
set_axis('up')

f.subplots_adjust(hspace=.1)

if args.p:
    plt.show()

if args.o:
    for file in args.o:
        plt.savefig(file)
    
plt.close()

