__author__ = 'zy'

class EpochalDisplacement(EpochalSitesFilteredData):
    def __init__(self,epoch_file,
                 filter_sites_file=None, filter_sites=None):
        super().__init__(epoch_file, filter_sites_file, filter_sites)

    def get_time_series(self, site, cmpt):
        epochs = self.get_epochs()
        ys = zeros_like(epochs,float)
        for nth, epoch in enumerate(epochs):
            tp = self.get_epoch_value_at_site(site, cmpt, epoch)
            ys[nth] = tp
        return ys

    def vstack(self, epochs):
        return vstack_column_vec(self, epochs)


def vstack_column_vec(epoch_data, epochs):
    res = epoch_data.get_data_at_epoch(epochs[0])
    assert_col_vec_and_get_nrow(res)
    for epoch in epochs[1:]:
        res = vstack((res,epoch_data.get_data_at_epoch(epoch)))
    return res