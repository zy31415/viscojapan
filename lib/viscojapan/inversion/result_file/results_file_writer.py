import numpy as np

class ResultFileWriter(FileIOBase):
    def __init__(self, inv, file_name):
        self.inv = inv
        super.__init__(file_name)

    def open(self):
        assert not exists(self.file_name)
        return h5py.File(self.file_name,'w')

    def save(self):
        inv = self.inv
        fid = self.fid

        # basic results:
        fid['m'] = inv.m
        fid['Bm'] = inv.Bm
        fid['d_pred'] = inv.d_pred

        # misfit information:
        fid['misfit/norm'] = inv.get_residual_norm()
        fid['misfit/rms'] = inv.get_residual_rms()
        fid['misfit/norm_weighted'] = inv.get_residual_norm_weighted()

        # regularization information
        for par, name in zip(inv.regularization.args,
                             inv.regularization.arg_names):
            fid['regularization/%s/coef'%name] = par

        for nsol, name in zip(self.regularization.components_solution_norms(self.Bm),
                              self.regularization.arg_names):
            fid['regularization/%s/norm'%name] = nsol

        # epochs:
        fid['epochs'] = inv.epochs
        fid['num_nlin_pars'] = inv.num_nlin_par
        for nth, pn in enumerate(inv.nlin_par_names):
            fid['nlin_pars/'+pn] = inv.Bm[nth - inv.num_nlin_par,0]

        sites = np.loadtxt(inv.filter_sites_file,'4a', usecols=(0,))
        ch_inland = vj.choose_inland_GPS_for_cmpts(sites)
        fid['sites'] = sites
        fid['misfit/rms_inland'] = inv.get_residual_rms(subset=ch_inland)

        if len(inv.epochs)>1:
            fid['misfit/rms_inland_at_epoch'] = inv._compute_rms_inland_at_each_epoch()
        
        
        

    
