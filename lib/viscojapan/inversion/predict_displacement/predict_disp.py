import numpy as np

from ...epochal_data import EpochalSitesFileReader, EpochalFileReader, DiffED, EpochalG
from ..result_file import SlipResultReader
from ...utils import as_string

__all__ = ['DispPred']

class DispPred(object):
    def __init__(self,
                 file_G0,                 
                 result_file,
                 fault_file,
                 files_Gs = None,
                 nlin_par_names = None,
                 file_incr_slip0 = None
                 ):
        self.result_file = result_file
        self.slip_result_reader = SlipResultReader(
            self.result_file,
            fault_file
            )
        self.sites_in_inversion = self.slip_result_reader.sites

        self.epochs = self.slip_result_reader.epochs
        self.num_epochs = len(self.epochs)

        self.file_G0 = file_G0
        self.file_G0_reader = EpochalSitesFileReader(
            epoch_file = self.file_G0,
            )
        
        self.files_Gs = files_Gs

        self._assert_all_G_files_have_the_same_sites_list()
        self.sites_for_prediction = self.file_G0_reader.filter_sites
        
        self.fault_file = fault_file
        
        self.nlin_par_names = nlin_par_names
        self.file_incr_slip0 = file_incr_slip0
        if self.files_Gs is not None:
            self._get_delta_nlin_pars()

    def _assert_all_G_files_have_the_same_sites_list(self):
        reader = EpochalFileReader(self.file_G0)
        sites = as_string(reader['sites'])

        for G in self.files_Gs:
            reader = EpochalFileReader(G)
            assert sites == as_string(reader['sites'])
        
    def _get_delta_nlin_pars(self):
        self.delta_nlin_pars = []
        for par in self.nlin_par_names:
            delta = self.slip_result_reader.get_nlin_par_val(par) - self.file_G0_reader[par]
            self.delta_nlin_pars.append(delta)        
        

    def E_cumu_slip(self, nth_epoch):
        cumuslip = self.slip_result_reader.get_total_slip_at_nth_epoch(nth_epoch)
        G0 = self.file_G0_reader[0]
        disp = np.dot(G0, cumuslip)
        if self.files_Gs is not None:
            disp += self._nlin_correction_E_cumu_slip(nth_epoch)
        return disp

    def _nlin_correction_E_cumu_slip(self, nth_epoch):
        reader = EpochalFileReader(self.file_incr_slip0)
        slip0 = reader[0]
        for nth in range(1, nth_epoch+1):
            epoch = int(self.epochs[nth])
            slip0 += reader[epoch]

        dGs = []
        for file_G, par in zip(self.files_Gs, self.nlin_par_names):
            G0 = EpochalG(self.file_G0)
            G = EpochalG(file_G)
            diffG = DiffED(ed1=G0, ed2=G, wrt=par)
            dGs.append(diffG[0])

        corr = None
        for dG, dpar in zip(dGs, self.delta_nlin_pars):
            if corr is None:
                corr  = np.dot(dG, slip0)*dpar
            else:
                corr += np.dot(dG, slip0)*dpar
        return corr
            
        
    def E_co(self):
        return self.E_cumuslip(0)

    def E_aslip(self, nth_epoch):
        aslip = self.slip_result_reader.get_after_slip_at_nth_epoch(nth_epoch)
        G0 = self.file_G0_reader[0]        
        disp = np.dot(G0, aslip)
        if self.files_Gs is not None:
            disp += self._nlin_correction_E_aslip(nth_epoch)
        return disp

    def _nlin_correction_E_aslip(self, nth_epoch):
        epoch = int(self.epochs[nth_epoch])
        slip0 = EpochalFileReader(self.file_incr_slip0)[epoch]
        
        dGs = []
        for file_G, par in zip(self.files_Gs, self.nlin_par_names):
            G0 = EpochalG(self.file_G0)
            G = EpochalG(file_G)
            diffG = DiffED(G0, G, par)
            dGs.append(diffG[0])

        corr = None
        for dG, dpar in zip(dGs, self.delta_nlin_pars):
            if corr is None:
                corr  = np.dot(dG, slip0)*dpar
            else:
                corr += np.dot(dG, slip0)*dpar
        return corr
        
    def R_nth_epoch(self, from_nth_epoch, to_epoch):
        epochs = self.epochs
        from_epoch = epochs[from_nth_epoch]

        del_epoch = to_epoch - from_epoch
        
        if del_epoch < 0:
            return np.zeros([self.file_G0_reader[0].shape[0],1])
        else:
            G = self.file_G0_reader[int(del_epoch)] - self.file_G0_reader[0]
            slip = self.slip_result_reader.get_incr_slip_at_nth_epoch(from_nth_epoch)
            disp = np.dot(G, slip)
            if self.files_Gs is not None:
                disp += self._nlin_correction_R_nth_epoch(from_nth_epoch, to_epoch)
            return disp

    def _nlin_correction_R_nth_epoch(self, from_nth_epoch, to_epoch):
        from_epoch = int(self.epochs[from_nth_epoch])
        slip0 = EpochalFileReader(self.file_incr_slip0)[from_epoch]

        del_epoch = int(to_epoch - from_epoch)
        
        dGs = []
        for file_G, par in zip(self.files_Gs, self.nlin_par_names):
            G0 = EpochalG(self.file_G0)
            G = EpochalG(file_G)
            diffG = DiffED(G0, G, par)
            dG0 = diffG[0]
            dG = diffG[del_epoch]
            dGs.append(dG-dG0)

        corr = None
        for dG, dpar in zip(dGs, self.delta_nlin_pars):
            if corr is None:
                corr  = np.dot(dG, slip0)*dpar
            else:
                corr += np.dot(dG, slip0)*dpar
        return corr

    def R_co(self, epoch):
        return self.R_nth_epoch(0, epoch)  

    def R_aslip(self, epoch):
        num_epochs = self.num_epochs
        disp = None
        for nth in range(num_epochs):
            if nth == 0:
                continue
            if disp is None:
                disp = self.R_nth_epoch(nth, epoch)
            else:
                disp += self.R_nth_epoch(nth, epoch)
        return disp




                
                

            
                
                
