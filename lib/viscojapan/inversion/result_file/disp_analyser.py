from .result_file_reader import ResultFileReader

class DispAnalyser(object):
    def __init__(self,
                 result_file):
        self.result_file = result_file
        self.result_file_reader = ResultFileReader(result_file)

        self.d_pred = self.result_file_reader.d_pred
        self.d_obs = self.result_file_reader.d_obs
        self.num_epochs = self.result_file_reader.num_epochs
        self.num_sites = self.result_file_reader.num_sites

    def get_pred_3d(self):
        return self.d_pred.reshape([self.num_epochs, self.num_sites, 3])

    def get_post_pred_3d(self):
        return self.d_pred.reshape([self.num_epochs, self.num_sites, 3])

    def get_obs_3d(self):
        return self.d_obs.reshape([self.num_epochs, self.num_sites, 3])

    def get_post_obs_3d(self):
        return self.d_obs.reshape([self.num_epochs, self.num_sites, 3])

    def get_rms(self, subset_epochs=None, subset_sites=None, subset_cmpt=None):
        d_pred = self.get_pred_3d()        
        d_obs = self.get_obs_3d()
        
        diff = d_pred - d_obs

        if subset_epochs is None:
            ch_epochs = np.s_[:]
        else:
            assert len(subset_epochs) == self.num_epochs

        if subset_sites is None:
            ch_sites = np.s_[:]
        else:
            assert len(ch_sites) == self.num_sites

        if subset_cmpt is None:
            ch_cmpt = np.s_[:]
        else:
            assert len(subset_cmpt) == 3

        diff = diff[ch_epochs, ch_sites, ch_cmpt]
        return np.sqrt(np.mean(diff**2))
