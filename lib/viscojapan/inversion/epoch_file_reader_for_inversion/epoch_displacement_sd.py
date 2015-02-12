__author__ = 'zy'

class EpochalDisplacementSD(EpochalSitesFilteredData):
    def __init__(self,epoch_file,
                 filter_sites_file=None, filter_sites=None):
        super().__init__(epoch_file, filter_sites_file, filter_sites)

    def vstack(self, epochs):
        return vstack_column_vec(self, epochs)


def vstack_column_vec(epoch_data, epochs):
    res = epoch_data.get_data_at_epoch(epochs[0])
    assert_col_vec_and_get_nrow(res)
    for epoch in epochs[1:]:
        res = vstack((res,epoch_data.get_data_at_epoch(epoch)))
    return res