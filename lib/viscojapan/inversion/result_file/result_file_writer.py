import os

import numpy as np
import h5py

from ...file_io_base import FileIOBase
from ...sites_db import choose_inland_GPS_cmpts_for_all_epochs,\
     choose_inland_GPS_cmpts_at_nth_epochs

class ResultFileWriter(FileIOBase):
    def __init__(self, inv, file_name):
        super().__init__(file_name)
        self.inv = inv

    def open(self):
        assert not os.path.exists(self.file_name)
        return h5py.File(self.file_name,'w')

    def save(self):
        inv = self.inv
        fid = self.fid

        # basic inputs:
        fid['d_obs'] = inv.disp_obs

        # basic results:
        fid['m'] = inv.m
        fid['Bm'] = inv.Bm
        fid['d_pred'] = inv.d_pred        

        # misfit information:
        self._save_misfit()
        
        # regularization information
        for par, name in zip(inv.regularization.args,
                             inv.regularization.arg_names):
            fid['regularization/%s/coef'%name] = par

        for nsol, name in zip(inv.regularization.components_solution_norms(inv.Bm),
                              inv.regularization.arg_names):
            fid['regularization/%s/norm'%name] = nsol
        
        self._save_non_linear_parameters()
        

    def _save_non_linear_parameters(self):
        inv = self.inv
        fid = self.fid
        
        num_nlin_pars = len(inv.nlin_par_names)
        fid['nlin_pars/num_nlin_pars'] = num_nlin_pars
        if num_nlin_pars > 0:
            fid['nlin_pars/num_nlin_par_names'] = inv.nlin_par_names
            fid['nlin_pars/nlin_par_initial_values'] = inv.nlin_par_initial_values
            fid['nlin_pars/nlin_par_solved_values'] = inv.Bm[-num_nlin_pars,0]

    def _save_misfit(self):
        inv = self.inv
        self.fid['misfit/norm'] = inv.get_residual_norm()
        self.fid['misfit/rms'] = inv.get_residual_rms()
        self.fid['misfit/norm_weighted'] = inv.get_residual_norm_weighted()

        self._save_inland_misfit()
        self._save_misfit_at_sites()

    def _save_inland_misfit(self):
        inv = self.inv
        fid = self.fid

        num_epochs = len(inv.epochs)

        fid['epochs'] = inv.epochs
        fid['sites'] = inv.sites
        ch_inland_sites = choose_inland_GPS_cmpts_for_all_epochs(inv.sites, num_epochs)
        fid['misfit/rms_inland'] = inv.get_residual_rms(subset = ch_inland_sites)
    
        rms_inland_at_epoch = []
        for nth, epoch in enumerate(inv.epochs):
            ch_inland_sites = choose_inland_GPS_cmpts_at_nth_epochs(
                inv.sites,
                nth,
                num_epochs
                )        
            rms_inland_at_epoch.append(inv.get_residual_rms(subset = ch_inland_sites))

        fid['misfit/rms_inland_at_epoch'] = np.asarray(rms_inland_at_epoch)

    def _save_misfit_at_sites(self):
        num_epochs = self.inv.num_epochs
        num_sites = len(self.inv.sites)
        d = self.inv.d_pred - self.inv.d        
        d = d.reshape((num_epochs, num_sites, 3))
        rms = np.sqrt((d**2).sum(axis=0)/num_epochs)
        self.fid['misfit/at_sites/e'] = rms[:,0]
        self.fid['misfit/at_sites/n'] = rms[:,1]
        self.fid['misfit/at_sites/u'] = rms[:,2]
        
        
