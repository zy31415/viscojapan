import viscojapan as vj

res_file = '../run2_seafloor_01/outs/nrough_14_ntop_02.h5'
fault_file = '../../fault_model/fault_bott60km.h5'
reader = vj.ResultFileReader(res_file)
slip = reader.slip

vj.pollitz.gen_subflts_input(fault_file, 'subflts', rake = 83., slip = slip)
