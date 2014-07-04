from viscojapan.fault_model import \
     SubfaultsMeshesByLength, SubfaultsMeshesByNumber

gen_subfault = SubfaultsMeshesByNumber(
    num_subflt_along_strike = 25,
    num_subflt_along_dip = 10,
    depth_bottom_limit = 50.
    )

gen_subfault.save_fault_file('fault.h5')

##gen_subflts_input_for_pollitz(
##    fault_file = 'fault.h5',
##    out_dir = 'subflts')
