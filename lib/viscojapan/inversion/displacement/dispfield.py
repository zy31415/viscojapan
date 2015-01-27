__author__ = 'zy'

class DispField(object):
    def __init__(self,
                 disp,
                 sites,
                 epochs,
                 ):
        self._displacement = disp
        self.sites = sites
        self.epochs = epochs

        self.num_epochs = epochs
        self.num_sites = len(self.sites)

        assert len(self._displacement.shape) == 3
        assert self._displacement.shape[0] == self.num_epochs
        assert self._displacement.shape[1] == self.num_sites
        # three components
        assert self._displacement.shape[3] == 3

    def get_coseismic_disp(self):
        return self._displacement[0,:,:]

    def get_cumu_disp_at_nth_epoch(self, nth):
        return self._displacement[nth,:,:]

    def get_post_disp_at_nth_epoch(self, nth):
        return self.get_cumu_disp_at_nth_epoch(nth) - self.get_coseismic_disp()

