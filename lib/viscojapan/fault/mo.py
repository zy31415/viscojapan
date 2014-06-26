import h5py
from numpy import log10, asarray

from viscojapan.epochal_data import EpochalIncrSlip

_fault_file='/home/zy/workspace/visinv2/flt_250/fault.h5'

class ComputeMoment(object):
    def __init__(self):
        self.fault_model_file = _fault_file
        
    def moment(self, slip):
        ''' Compute moment.
'''
        with h5py.File(self.fault_model_file) as fid:
            fl=float(fid['subflt_len'][...])
            fw=float(fid['subflt_wid'][...])
            shr=fid['meshes/shear'][...]
        mos = shr.flatten()*slip.flatten()*fl*1e3*fw*1e3
        mo = sum(mos)
        mw = 2./3.*log10(mo)-6. 
        return mo, mw

def get_mos_mws_from_epochal_file(epochal_file):
    slip = EpochalIncrSlip(epochal_file)
    epochs = slip.get_epochs()

    mws = []
    mos = []
    for epoch in epochs:
        alpha = slip.get_info('alpha')
        s = slip.get_epoch_value(epoch)

        M = ComputeMoment()
        mo,mw = M.moment(s)
        mws.append(mw)
        mos.append(mo)
    return asarray(mos), asarray(mws), asarray(epochs)
