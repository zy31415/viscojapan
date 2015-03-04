import numpy as np

import glob

files = sorted(glob.glob('outs/*'),
               key = lambda f : int(f.split('_')[-3]))

sites = np.loadtxt('near_stations.in','4a', usecols=(0,))
sites = [site.decode() for site in sites]

def load(fn, site, cmpt):
    idx = sites.index(site)
    if cmpt=='e':
        c = 2
    elif cmpt=='n':
        c = 3
    elif cmpt=='u':
        c = 4
    return np.loadtxt(fn)[idx,c]


def get_ts(site, cmpt):
    epochs = []
    ys = []
    for f in files:
        epochs.append(int(f.split('_')[-3]))
        ys.append(load(f,site,cmpt))

    return epochs, ys

def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)

site = 'J543'
cmpt = 'u'

epochs, ys = get_ts(site, cmpt)

vel = np.diff(ys)/np.diff(epochs)

from pylab import plt

fig, ax1 = plt.subplots()

pos1 = ax1.get_position() # get the original position 
pos2 = [pos1.x0, pos1.y0,  pos1.width/1.1 , pos1.height] 
ax1.set_position(pos2)

ax1.plot(np.asarray(epochs)/365., ys,'bx-',
         label='disp.')
ax1.legend(loc=0)
#ax1.set_ylim([-1e-6,2e-6])
#
#######################

ax2 = ax1.twinx()
ax2.plot(np.asarray(epochs[1:])/365., vel*365,'r',
         label=r'vel ($yr^{-1}$)')
#ax2.set_xlim([0,10])
ax2.set_ylabel(r'$yr^{-1}$')
#ax2.set_ylim([-1e-6, 2e-6])

ax2.legend(loc=0)

ax2.set_position(pos2)

align_yaxis(ax1, 0, ax2, 0)


plt.title('%s - %s'%(site, cmpt))

##################33
###################

files = sorted(glob.glob('../outs/*'),
               key = lambda f : int(f.split('_')[-3]))

sites = np.loadtxt('../stations.in','4a', usecols=(0,))
sites = [site.decode() for site in sites]

def load(fn, site, cmpt):
    idx = sites.index(site)
    if cmpt=='e':
        c = 2
    elif cmpt=='n':
        c = 3
    elif cmpt=='u':
        c = 4
    return np.loadtxt(fn)[idx,c]


def get_ts(site, cmpt):
    epochs = []
    ys = []
    for f in files:
        epochs.append(int(f.split('_')[-3]))
        ys.append(load(f,site,cmpt))

    return epochs, ys

def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)

epochs, ys = get_ts(site, cmpt)

vel = np.diff(ys)/np.diff(epochs)

ax1.plot(np.asarray(epochs)/365., ys,'bx-',
         label='disp.')
ax1.legend(loc=0)
#ax1.set_ylim([-1e-6,2e-6])
#
#######################

ax2 = ax1.twinx()
ax2.plot(np.asarray(epochs[1:])/365., vel*365,'r',
         label=r'vel ($yr^{-1}$)')
#ax2.set_xlim([0,10])
ax2.set_ylabel(r'$yr^{-1}$')
#ax2.set_ylim([-1e-6, 2e-6])

ax2.legend(loc=0)

ax2.set_position(pos2)

align_yaxis(ax1, 0, ax2, 0)


plt.title('%s - %s'%(site, cmpt))









plt.savefig('%s_%s.png'%(site, cmpt))
plt.xlabel('year')
plt.grid('on')

###########

plt.show()
plt.close()
