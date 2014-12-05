import viscojapan as vj

vj.gmt.plot_slip_result(
    fault_file = '../../../fault_model/fault_bott60km.h5',
    result_file = '../../outs/nrough_06.h5',
    out_file = 'slip.pdf',
    subplot_width = 3.2,
    subplot_height = 5.2,
    num_plots_per_row = 5
    )
