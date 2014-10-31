import viscojapan as vj

mplt = vj.plots.MapPlotFault('../../../fault_model/fault_bott60km.h5')
mplt.plot_slip_file('slip0.h5',0)
vj.plots.plt.savefig('initial_slip_input.png')
vj.plots.plt.show()
