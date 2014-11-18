import viscojapan as vj

fault_file = '../../fault_model/fault_bott60km.h5'
vj.pollitz.gen_subflts_input(fault_file, 'subflts', rake = 83.)
