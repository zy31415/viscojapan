import viscojapan as vj

reader = vj.inv.ResultFileReader('nco_06_naslip_10.h5')
num_nlin_pars = reader.num_nlin_pars
m = reader.m
epochs = reader.epochs
epoch_file = '~slip0.h5'

vj.break_col_vec_into_epoch_file(m[:-num_nlin_pars,:], epochs, epoch_file)
    
reader = vj.EpochalFileReader('~slip0.h5')
epochs = reader.get_epochs()

with vj.EpochalFileWriter('slip0.h5') as writer:
    for epoch in epochs:
        m = reader[epoch]
        writer[epoch] = m[:336,:]
    writer.copy_info_from('~slip0.h5')
