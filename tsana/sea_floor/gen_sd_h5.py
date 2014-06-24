from numpy import loadtxt, asarray

from viscojapan.epochal_data import EpochalData

tp = loadtxt('sites_with_seafloor_sd','4a,3f')
sites = asarray([ii[0] for ii in tp])
sd_arr = asarray([ii[1] for ii in tp])
sd = sd_arr.reshape([-1,1])

ep = EpochalData('sd_with_seafloor.h5')

for epoch in range(0,1200):
    ep.set_epoch_value(epoch,sd)

ep.set_info('sites', sites)
