from pylab import plt

import viscojapan as vj

fn = '../../outs/nrough_05_naslip_11.h5'

reader = vj.inv.ResultFileReader(fn)


slip = reader.get_slip()

nx = 6
ny = 13
vj.slip.plot.plot_slip_and_rate_at_subflt(slip, nx, ny)

plt.savefig('subflt_%02d_%02d.png'%(nx, ny))
plt.show()
