import viscojapan as vj

plt = vj.gmt.PlotSlipResult(
    fault_file = '../../../fault_model/fault_bott60km.h5',
    result_file = '../../outs0/nco_06_naslip_10.h5',
    subplot_width = 3.2,
    subplot_height = 5.2,
    num_plots_per_row = 5,
    earth_file = '../../../earth_model_nongravity/He50km_VisM6.3E18/earth.model_He50km_VisM6.3E18'
    )
plt.plot('slip.pdf')
plt.clean()
