import viscojapan as vj

g = vj.inv.ep.EpochG('../G_large_scale.h5')

site = 'X3D7'
cmpt = 'n'

nth_subflt = 100

epochs = g.get_epochs()

y = g.cumu_ts(site, cmpt, nth_subflt)

from pylab import plt

plt.plot(epochs, y,'x-')
plt.show()
