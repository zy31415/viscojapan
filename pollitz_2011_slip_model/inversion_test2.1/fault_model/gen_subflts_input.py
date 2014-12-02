import viscojapan as vj

vj.pollitz.gen_subflts_input_point_source(
    fault_file = 'fault_bott50km.h5',
    out_dir = 'subflts_rake90',
    rake = 90.)

vj.pollitz.gen_subflts_input_point_source(
    fault_file = 'fault_bott50km.h5',
    out_dir = 'subflts_rake81',
    rake = 81.)
