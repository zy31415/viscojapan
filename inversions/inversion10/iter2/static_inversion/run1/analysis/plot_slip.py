import viscojapan as vj

fault_file = '../../fault_model/fault_bott80km.h5'
epoch = 1344
with vj.inv.ResultFileReader('../outs/outs_%04d/rough_06.h5'%epoch,) as reader:
    slip = reader.incr_slip

mplt = vj.plots.MapPlotFault(fault_file)


mplt.plot_slip(slip)

vj.plots.plt.show()
