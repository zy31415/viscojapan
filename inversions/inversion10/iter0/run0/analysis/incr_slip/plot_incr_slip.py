import viscojapan as vj

for nrough in range(19):        
    plt = vj.gmt.PlotSlipResult(
        fault_file = '../../../fault_model/fault_bott120km.h5',
        result_file = '../../outs/nrough_%02d.h5'%(nrough),
        subplot_width = 3.2,
        subplot_height = 5.2,
        num_plots_per_row = 5,
        earth_file = '../../../earth_model_nongravity/He50km_VisM6.3E18/earth.model_He50km_VisM6.3E18',
        color_label_interval_aslip = .3,
        )
    plt.plot('plots/nrough_%02d.pdf'%nrough)
    plt.clean()
