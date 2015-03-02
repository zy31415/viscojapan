from viscojapan.pollitz import gen_subflts_input

dep = 80

rake1 = 84
rake2 = 85


def gen(rake):
    gen_subflts_input(
        fault_file = 'fault_bott%dkm.h5'%dep,
        out_dir = 'subflts_bott%dkm_rake%d'%(dep, rake),
        rake = rake)

gen(rake1)
gen(rake2)
