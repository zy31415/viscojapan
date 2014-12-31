import numpy as np

from .result_file_reader import ResultFileReader

__all__ = ['DispResultReader']

class DispResultReader(ResultFileReader):
    def __init__(self,
                 result_file):
        super().__init__(result_file)        
        
    def get_cumu_pred_3d(self):
        return self.d_pred.reshape([self.num_epochs, self.num_sites, 3])

    def get_post_pred_3d(self):
        disp = self.get_cumu_pred_3d()
        return disp - disp[0,:,:]

    def get_cumu_obs_3d(self):
        return self.d_obs.reshape([self.num_epochs, self.num_sites, 3])

    def get_post_obs_3d(self):
        disp = self.get_cumu_obs_3d()
        return disp - disp[0,:,:]

    def _get_rms(self, d_pred, d_obs,
                 subset_epochs=None, subset_sites=None, subset_cmpt=None,
                 axis = None):    
        diff = d_pred - d_obs

        if subset_epochs is None:
            ch_epochs = np.s_[:]
        else:
            ch_epochs =  np.asarray(subset_epochs)

        if subset_sites is None:
            ch_sites = np.s_[:]
        else:
            ch_sites =  np.asarray(subset_sites)

        if subset_cmpt is None:
            ch_cmpt = np.s_[:]
        else:
            ch_cmpt = np.asarray(subset_cmpt)

        diff = diff[ch_epochs, ch_sites, ch_cmpt]
        return np.sqrt(np.mean(diff**2, axis = axis))


    def get_cumu_rms(self,
                     subset_epochs=None, subset_sites=None, subset_cmpt=None,
                     axis = None):
        d_pred = self.get_cumu_pred_3d()        
        d_obs = self.get_cumu_obs_3d()
        return self._get_rms(d_pred = d_pred,
                             d_obs = d_obs,
                             subset_epochs=subset_epochs,
                             subset_sites=subset_sites,
                             subset_cmpt=subset_cmpt,
                             axis = axis
                             )

    def get_post_rms(self,
                     subset_epochs=None, subset_sites=None, subset_cmpt=None,
                     axis = None):
        d_pred = self.get_post_pred_3d()        
        d_obs = self.get_post_obs_3d()
        
        return self._get_rms(d_pred, d_obs,
                             subset_epochs=subset_epochs,
                             subset_sites=subset_sites,
                             subset_cmpt=subset_cmpt,
                             axis = axis
                             )

    def get_ts_cumu_pred(self,site, cmpt):
        disp = self.get_cumu_pred_3d()
        index = self.sites.index(site)
        if cmpt == 'e':
            ts = disp[:,index,0]
        elif cmpt == 'n':
            ts = disp[:,index,1]
        elif cmpt == 'u':
            ts = disp[:,index,2]
        else:
            raise ValueError()
        return ts.flatten(), self.epochs

    def get_cumu_pred_at_nth_epoch(self, nth_epoch):
        disp = self.get_cumu_pred_3d()
        return disp[nth_epoch,:,:]
    
