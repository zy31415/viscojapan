from viscojapan.pollitz import gen_subflts_input

dep = 80

rake = 83.98

gen_subflts_input(
    fault_file = 'fault_bott%dkm.h5'%dep,
    out_dir = 'subflts/',
    rake = rake)

