import viscojapan as vj

from pylab import plt

partition_file = './deformation_partition_large_scale.h5'
result_file = '../../outs/nrough_06_naslip_11.h5'

plotter = vj.inv.PredictedTimeSeriesPlotter(
    partition_file = partition_file,
    result_file = result_file,
    )

site = 'X375'

cmpt='e'
plotter.plot_R_co(site,cmpt, label='Rco')
plotter.plot_E_aslip(site,cmpt, label='Easlip')
plotter.plot_R_aslip(site,cmpt, label='Raslip')
#plotter.plot_cumu_disp_pred_added(site, cmpt, color='blue')
plt.legend()
plt.show()
plt.close()
    

