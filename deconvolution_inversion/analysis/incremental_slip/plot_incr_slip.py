from pylab import show, savefig, close

from viscojapan.plot_epochal_data.plot_slip import PlotIncrSlip

from days import days as epochs

ano = 14

for epoch in epochs:
    plot = PlotIncrSlip()
    plot('../../outs0/slip_%02d.h5'%ano, epoch)
    savefig('incr_slip_%04d.png'%epoch)
    close()
