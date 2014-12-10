import numpy as np

from ...epochal_data import EpochalSitesFileReader
from ..result_file import ResultFileReader

__all__ = ['DispPred']

class DispPred(object):
    def __init__(self,
                 G_file,                 
                 result_file,
                 fault_file,        
                 ):
        self.result_file = result_file
        self.result_file_reader = ResultFileReader(
            self.result_file,
            fault_file
            )
        self.filter_sites = self.result_file_reader.sites

        self.G_file = G_file
        self.G_reader = EpochalSitesFileReader(
            epoch_file = self.G_file,
            filter_sites = self.filter_sites,
            )

        self.epochs = self.result_file_reader.epochs
        self.num_epochs = len(self.epochs)

        self.fault_file = fault_file

    def E_cumu_slip(self, nth_epoch):
        cumuslip = self.result_file_reader.get_total_slip_at_nth_epoch(nth_epoch)
        G0 = self.G_reader[0]
        disp = np.dot(G0, cumuslip)
        return disp
        
    def E_co(self):
        return self.E_cumuslip(0)

    def E_aslip(self, nth_epoch):
        aslip = self.result_file_reader.get_after_slip_at_nth_epoch(nth_epoch)
        G0 = self.G_reader[0]        
        disp = np.dot(G0, aslip)
        return disp
        
    def R_nth_epoch(self, from_nth_epoch, to_epoch):
        epochs = self.result_file_reader.epochs
        from_epoch = epochs[from_nth_epoch]

        del_epoch = to_epoch - from_epoch
        
        if del_epoch < 0:
            return np.zeros([self.G_reader[0].shape[0],1])
        else:
            G = self.G_reader[int(del_epoch)] - self.G_reader[0]
            slip = self.result_file_reader.get_incr_slip_at_nth_epoch(from_nth_epoch)
            disp = np.dot(G, slip)
            return disp

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




                
                

            
                
                
