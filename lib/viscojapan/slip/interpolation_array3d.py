import numpy as np

__author__ = 'zy'
__all__ = ['interpolation_array3d']

def interpolation_array3d(arr3d, epochs, epoch):
    arr3d = np.asarray(arr3d)

    _assert_ascending(epochs)
    epochs = list(epochs)

    assert len(arr3d.shape) == 3
    assert arr3d.shape[0] == len(epochs)
    _assert_within_range(epochs, epoch)
    # nth = int(nth)
    # assert nth>=0
    # assert nth < self.num_epochs
    #
    # return self.cumu_slip3d[nth,:,:]nth

    if epoch in epochs:
        nth = epochs.index(epoch)
        return arr3d[nth, :, :]

    for nth, ti in enumerate(epochs[1:]):
        if epoch <= ti:
            break

    t1 = epochs[nth]
    t2 = epochs[nth+1]

    assert (t1<t2) and (t1<=epoch) and (epoch<=t2), 'Epoch %d should be in %d ~ %d'%(epoch, t1, t2)

    G1 = arr3d[nth, :, :]
    G2 = arr3d[nth, :, :]

    G=(epoch-t1)/(t2-t1)*(G2-G1)+G1

    return G

def _assert_within_range(epochs,epoch):
    max_day = max(epochs)
    min_day = min(epochs)
    assert epoch <= max_day, 'Max day: %d'%max_day
    assert epoch >= min_day, 'Min day: %d'%min_day

def _assert_ascending(arr):
    assert all(arr[i] <= arr[i+1] for i in range(len(arr)-1))