import numpy as np

from ..fault_model import FaultFileReader
from ..earth_model import EarthModelFileReader

from .utils import mo_to_mw

__all__ = ['MomentCalculator']


class MomentCalculator(object):
    def __init__(self, fault_file, earth_file):
        self.fault_model_file = fault_file
        self.earth_model_file = earth_file

    def get_shear(self):
        reader = FaultFileReader(self.fault_model_file)
        ddeps = reader.ddeps[1:, 1:]
        reader = EarthModelFileReader(self.earth_model_file)
        return reader.get_shear_by_dep(ddeps)
        
        
    def compute_moment(self, slip2d):
        ''' Compute moment.
'''
        reader = FaultFileReader(self.fault_model_file)
        
        fl = reader.subflt_sz_dip
        fw = reader.subflt_sz_strike
        
        shr = self.get_shear()
        mos = shr.flatten()*slip2d.flatten()*fl*1e3*fw*1e3
        mo = np.sum(mos)
        mw = mo_to_mw(mo)
        return mo, mw

    def get_cumu_slip_Mos_Mws(self, slip):
        return self._get_Mos_Mws(slip3d=self.slip.get_3d_cumu_slip())

    def get_afterslip_Mos_Mws(self, slip):
        return self._get_Mos_Mws(slip3d=self.slip.get_3d_afterslip())

    def _get_Mos_Mws(self, slip3d):
        epochs = slip3d.epochs
        mos = []
        mws = []
        for nth, epoch in enumerate(epochs):
            si = slip3d[nth,:,:]
            mo, mw = self.compute_moment(slip2d=si)
            mos.append(mo)
            mws.append(mw)
        return mos, mws, epochs

def get_mos_mws_from_epochal_file(epochal_file):
    slip = EpochalIncrSlip(epochal_file)
    epochs = slip.get_epochs()

    mws = []
    mos = []
    for epoch in epochs:
        alpha = slip.get_info('alpha')
        s = slip.get_epoch_value(epoch)

        M = MomentCalculator()
        mo,mw = M.moment(s)
        mws.append(mw)
        mos.append(mo)
    return asarray(mos), asarray(mws), asarray(epochs)
