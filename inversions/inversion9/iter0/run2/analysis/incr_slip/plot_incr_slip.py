import viscojapan as vj

for nco in range(4,8):
    for naslip in range(5, 12):
        plt = vj.gmt.PlotSlipResult(
            fault_file = '../../../fault_model/fault_bott60km.h5',
            result_file = '../../outs0/nco_%02d_naslip_%02d.h5'%(nco, naslip),
            subplot_width = 3.2,
            subplot_height = 5.2,
            num_plots_per_row = 5,
            earth_file = '../../../earth_model_nongravity/He50km_VisM6.3E18/earth.model_He50km_VisM6.3E18',
            color_label_interval_aslip = .3,
            )
        plt.plot('plots/slip_nco_%02dd_naslip_%02d.pdf'%(nco, naslip))
        plt.clean()
