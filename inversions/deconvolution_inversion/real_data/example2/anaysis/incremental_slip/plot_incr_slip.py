from pylab import show, savefig, close

from viscojapan.plot_epochal_data.plot_slip import PlotIncrSlip

from epochs_log import epochs

ano = 10
bno = 00
for epoch in epochs:
    print(epoch)
    plot = PlotIncrSlip()
    plot('../../outs_log/incr_slip_a%02d_b%02d.h5'%(ano,bno), epoch)
    savefig('plots/incr_slip_%04d.png'%epoch)
    #show()
    close()
