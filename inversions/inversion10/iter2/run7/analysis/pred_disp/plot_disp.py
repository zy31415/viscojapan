import viscojapan as vj

from pylab import plt

partition_file = './deformation_partition.h5'
result_file = '../../outs/nrough_05_naslip_11.h5'

plotter = vj.inv.PredictedTimeSeriesPlotter(
    partition_file = partition_file,
    result_file = result_file,
    )

site = 'J550'
cmpt = 'e'
plotter.plot_cumu_disp_decomposition(site, cmpt, added_label='added')
plotter.plot_cumu_disp_pred_added(site, cmpt, color='blue')
plt.show()
plt.close()
    
