import numpy as np
import h5py

import viscojapan as vj

__all__ = ['DeformationDecomposition']

class DeformationDecomposition(object):
    def __init__(self,
                 f_res,
                 file_G0,
                 files_Gs,
                 sites_file,
                 epochs,
                 nlin_par_names,                 
                 ):
        self.f_res = f_res
        self.file_G0 = file_G0        
        self.files_Gs = files_Gs
        self.nlin_par_names = nlin_par_names
        self.num_nlin_pars = len(nlin_par_names)
        self.sites_file = sites_file
        self.sites = np.loadtxt(sites_file,'4a,')
        self.num_obs = len(self.sites)*3
        self.epochs = epochs
        self.num_epochs = len(epochs)

        self.ep_G0 = vj.EpochalG(file_G0, sites_file)
        self.ep_Gs = []
        for f_G in self.files_Gs:
            self.ep_Gs.append(vj.EpochalG(f_G, sites_file))

        self._read_result_file()

    def _read_result_file(self):
        with h5py.File(self.f_res) as fid:
            Bm = fid['Bm'][...]
            d_pred = fid['d_pred'][...]
        self.d_pred = d_pred
        self.slip = Bm[:-self.num_nlin_pars,0].reshape([self.num_epochs, -1,1])
        self.nlin_pars =Bm[-self.num_nlin_pars:,0]

    def compute_elastic_disp(self, nth_epoch):
        G0 = self.ep_G0[0]
        slip = self.slip[nth_epoch,:,:]
        d = np.dot(G0,slip)
        cor = self._correct_nlin_par(slip,0)
        d += cor
        return d

    def gen_total_disp_file(self,fn):
        ds = self.d_pred.reshape([self.num_epochs,-1])
        self._save_ds(ds.T, fn)

    def gen_elastic_file(self,fn):
        ds = []
        for nth_epoch in range(self.num_epochs):
            d = self.compute_elastic_disp(nth_epoch)
            if ds == []:
                ds.append(d.reshape([-1]))
            else:
                ds.append(ds[-1]+d.reshape([-1]))
        ds = np.asarray(ds).T             
        self._save_ds(ds,fn)

    def compute_relax_disp(self, nth_epoch):
        epoch0 = self.epochs[nth_epoch]
        slip = self.slip[nth_epoch,:,:]
        ds = np.zeros([self.num_obs, self.num_epochs])

        d_co = self.compute_elastic_disp(nth_epoch)
        
        for n, epoch in enumerate(self.epochs):
            if n <= nth_epoch:
                continue
            G = self.ep_G0[epoch-epoch0]
            d = np.dot(G, slip)
               
            cor1 = self._correct_nlin_par(slip, epoch-epoch0) 
            d += cor1
            d_relax = d - d_co
            ds[:, n] = d_relax[:,0]
        return ds

    def gen_co_relax_file(self,fn):
        ds = self.compute_relax_disp(0)
        self._save_ds(ds,fn)
                
    def gen_aslip_relax_file(self,fn):
        ds = []
        for nth, epoch in enumerate(self.epochs):
            if nth == 0:
                continue
            print('Relaxation for %dth day.'%epoch)
            tp = self.compute_relax_disp(nth)
            if ds == []:
                ds = tp
            else:
                ds += tp
        self._save_ds(ds,fn)
        
    def _save_ds(self, ds, fn):
        with open(fn,'wt') as fid:
            fid.write('#site cmpt day = %d '%self.epochs[0])
            for epoch in self.epochs[1:]:
                fid.write('%13d '%epoch)
            fid.write('\n')
            
            for nth, di in enumerate(ds):
                n_site = nth//3
                n_cmpt = nth%3
                site = self.sites[n_site]
                cmpt = ['e','n','u'][n_cmpt]
                fid.write('%s %s '%(site.decode(),cmpt))
                for ii in di:
                    fid.write('%13E '%ii)
                fid.write('\n')

    def _correct_nlin_par(self, slip, t):
        out = self._correct_nth_nlin_par(0, slip, t)
        for nth in range(self.num_nlin_pars)[1:]:
            out += self._correct_nth_nlin_par(nth, slip, t)
        return out
            
    def _correct_nth_nlin_par(self, nth_npar, slip, epoch):        
        npar_name = self.nlin_par_names[nth_npar]
        
        ed1 = self.ep_G0
        ed2 = self.ep_Gs[nth_npar]
        diffG = vj.DiffED(ed1=ed1, ed2=ed2, wrt=npar_name)

        dG = diffG.get_epoch_value(epoch)

        npar_old = ed1[npar_name]
        npar_new = self.nlin_pars[nth_npar]
        dnpar = npar_new - npar_old
        delta_d = np.dot(dG, slip) * dnpar
        return delta_d


    
