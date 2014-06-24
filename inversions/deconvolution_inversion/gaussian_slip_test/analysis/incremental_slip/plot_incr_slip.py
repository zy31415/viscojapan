from pylab import show, savefig, close

from viscojapan.plot_epochal_data.plot_slip import PlotIncrSlip

from epochs_even import epochs

ano = 16
bno = 21
for epoch in epochs:
    print(epoch)
    plot = PlotIncrSlip()
    plot('../../outs_alpha_beta/incr_slip_a%02d_b%02d.h5'%(ano,bno), epoch)
    savefig('plots/incr_slip_%04d.png'%epoch)
    #show()
    close()
