from viscojapan.pollitz import gen_subflts_input

dep = 80

gen_subflts_input(
    fault_file = 'fault_bott%dkm.h5'%dep,
    out_dir = 'subflts_bott%dkm_rake83'%dep,
    rake = 83)

gen_subflts_input(
    fault_file = 'fault_bott%dkm.h5'%dep,
    out_dir = 'subflts_bott%dkm_rake90'%dep,
    rake = 90.)
