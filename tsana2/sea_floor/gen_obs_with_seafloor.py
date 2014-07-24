from numpy import loadtxt, insert

from viscojapan.epochal_data import EpochalData
from viscojapan.utils import _assert_assending_order

sites_with_seafloor = loadtxt('sites_with_seafloor','4a')

def insert_seafloor(arr):    
    _assert_assending_order(list(sites_with_seafloor))

    tp = loadtxt('sites_seafloor','4a, 2f, 3f, d')
    sites_seafloor = [ii[0] for ii in tp]
    obs_seafloor = [ii[2] for ii in tp]

    for site, obsi in zip(sites_seafloor, obs_seafloor):
        idx = list(sites_with_seafloor).index(site)
        arr = insert(arr,idx, obsi, axis=0)

    return arr

obs_obj = EpochalData('../post_fit/cumu_post.h5')
obs_obj_with_seafloor = EpochalData('cumu_post_with_seafloor.h5')
epochs = obs_obj.get_epochs()
for epoch in epochs:
    print(epoch)
    obs = obs_obj(epoch).reshape([-1, 3])
    obs = insert_seafloor(obs)

    obs_obj_with_seafloor.set_epoch_value(epoch, obs.reshape([-1,1]))

obs_obj_with_seafloor.set_info('sites', sites_with_seafloor)

    

    
    
    

    
