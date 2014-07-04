from viscojapan.fault_model import \
     SubfaultsMeshesByLength
from viscojapan.pollitz import gen_subflts_input_for_pollitz

gen_subfault = SubfaultsMeshesByLength(
    subflt_sz_dip = 20.,
    depth_bottom_limit = 50.,
    subflt_sz_strike = 20.
    )

# gen_subfault.save_fault_file('fault.h5')

gen_subflts_input_for_pollitz(
    fault_file = 'fault.h5',
    out_dir = 'subflts')
