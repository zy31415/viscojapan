import viscojapan as vj

from pylab import plt

partition_file = './deformation_partition.h5'
result_file = '../../outs/nrough_06_naslip_06.h5'

plotter = vj.inv.PredictedTimeSeriesPlotterNoRaslip(
    partition_file = partition_file,
    result_file = result_file,
    )

site = 'J551'
cmpt = 'u'
plotter.plot_cumu_disp(site, cmpt, added_label='added')
plotter.plot_cumu_disp_pred_added(site, cmpt, color='blue')
plt.show()
plt.close()
    
