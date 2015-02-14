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
plotter.plot_cumu_disp(site, cmpt, added_label='added')
plt.show()
plt.close()
    
