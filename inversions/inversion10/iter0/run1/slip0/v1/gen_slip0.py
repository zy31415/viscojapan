import viscojapan as vj

reader = vj.inv.ResultFileReader('nco_06_naslip_10.h5')
num_nlin_pars = reader.num_nlin_pars
m = reader.m
epochs = reader.epochs
epoch_file = 'slip0.h5'

vj.break_col_vec_into_epoch_file(m[:-num_nlin_pars,:], epochs, epoch_file)
    
