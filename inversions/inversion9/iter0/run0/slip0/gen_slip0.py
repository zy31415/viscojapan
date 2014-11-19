import h5py
import numpy as np

import viscojapan as vj

def patch_slip(slip):
    slip = slip.reshape([10, 35])

    slip_ = np.zeros([13,35])
    slip_[:10,:]  = slip
    return slip_
    

reader = vj.EpochalFileReader('incr_slip0.h5')
epochs = reader.get_epochs()

with vj.EpochalFileWriter('incr_slip0_patched.h5') as writer:
    for epoch in epochs:
        slip = reader[epoch]
        slip_ = patch_slip(slip)
        writer.set_epoch_value(epoch, slip_.reshape([-1,1]))

        #writer[epoch] = slip_
        
    


