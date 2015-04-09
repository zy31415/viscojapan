import viscojapan as vj

from epochs import epochs

fault_file = '../../../fault_model/fault_bott80km.h5'

for epoch in epochs[1:]:
    with vj.inv.ResultFileReader('../outs/outs_%04d/naslip_10.h5'%epoch,) as reader:
        slip = reader.incr_slip

    mplt = vj.plots.MapPlotFault(fault_file)
    mplt.plot_slip(slip)
    vj.plots.plt.show()
