import viscojapan as vj

reader = vj.inv.ResultFileReader('nrough_05_naslip_11.h5')
num_nlin_pars = reader.num_nlin_pars
Bm = reader.Bm

slip0 = Bm[:-num_nlin_pars,:]

epochs = reader.epochs
epoch_file = 'slip0.h5'

vj.break_col_vec_into_epoch_file(slip0, epochs, epoch_file)
    


