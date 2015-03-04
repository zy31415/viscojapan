import numpy as np
import h5py

import viscojapan as vj

fid1 = h5py.File('../disp.h5','r')
disp1 = vj.epoch_3d_array.Displacement.load(fid1)

fid2 = h5py.File('../one_soft_channel_model/disp.h5','r')
disp2 = vj.epoch_3d_array.Displacement.load(fid2)


def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)

site = 'J550'
cmpt = 'e'

ys1 = disp1.post_ts(site, cmpt)
vel1 = disp1.vel_ts(site, cmpt)*365
ts1 = np.asarray(disp1.get_epochs(), float)/365.

ys2 = disp2.post_ts(site, cmpt)
vel2 = disp2.vel_ts(site, cmpt)*365
ts2 = np.asarray(disp2.get_epochs(), float)/365.

############
# Start to plot

from pylab import plt

fig, ax1 = plt.subplots()

pos1 = ax1.get_position() # get the original position 
pos2 = [pos1.x0, pos1.y0,  pos1.width/1.1 , pos1.height] 
ax1.set_position(pos2)

ln1 = ax1.plot(ts1, ys1,'bx-', label='disp.')
ln2 = ax1.plot(ts2, ys2,'gx-', label='disp. - one channel')

#ax1.set_ylim([-1e-6,2e-6])

#####################

ax2 = ax1.twinx()

ln3 = ax2.plot(ts1[1:], vel1, 'r', label=r'vel ($yr^{-1}$)')
ln4 = ax2.plot(ts2[1:], vel2, color='brown', label=r'vel ($yr^{-1}$)  - one channel')

#ax2.set_xlim([0,10])
ax2.set_ylabel(r'$yr^{-1}$')
#ax2.set_ylim([-1e-6, 2e-6])

ax2.set_position(pos2)

align_yaxis(ax1, 0, ax2, 0)


lns = ln1 + ln2 + ln3 + ln4
labs = [l.get_label() for l in lns]

plt.legend(lns, labs, loc=5,prop={'size':6})

plt.title('%s - %s'%(site, cmpt))
plt.savefig('%s_%s.png'%(site, cmpt))
plt.xlabel('year')
plt.grid('on')

#########

plt.show()
plt.close()

