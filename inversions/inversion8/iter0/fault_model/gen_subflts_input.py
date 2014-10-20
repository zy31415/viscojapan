from viscojapan.pollitz import gen_subflts_input_for_pollitz

gen_subflts_input_for_pollitz(
    fault_file = 'fault_bott40km.h5',
    out_dir = 'subflts_bott40km_rake81',
    rake = 80.6)

gen_subflts_input_for_pollitz(
    fault_file = 'fault_bott40km.h5',
    out_dir = 'subflts_bott40km_rake90',
    rake = 90.)
