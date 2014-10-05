import viscojapan as vj


ep = vj.EpochalIncrSlip('incr_slip0.h5')

for epoch in ep.get_epochs():
    print(epoch)
    slip = ep[epoch]
    mplt = vj.MapPlotFault('../fault_model/fault_bott50km.h5')
    mplt.plot_slip(slip)
    vj.plt.savefig('plots/%04d.png'%epoch)
    vj.plt.close()
