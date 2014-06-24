import re

from numpy import loadtxt, asarray, inf, insert

from viscojapan.epochal_data import EpochalData

tp = loadtxt('sites_with_seafloor','4a')
sites_with_seafloor = [ii.decode() for ii in tp]


def seafloor_site_index(site):
    return list(sites_with_seafloor).index(site)

def seafloor_site_sd(site, epoch):
    with open('seafloor_sd','rt') as fid:
        records = re.findall('^\S*%s.*'%site, fid.read(), re.M)
    for record in records:
        tp = record.split()
        day = int(tp[1])
        val = tp[2:]
        if day == epoch:
            return asarray(val, float)
    return asarray((+inf, +inf, +inf), float)

def invert_seafloor_sd(arr, epoch):
    tp = loadtxt('sites_seafloor', '4a')
    sites = [ii.decode() for ii in tp]
    for site in sites:
        idx = seafloor_site_index(site)
        val = seafloor_site_sd(site, epoch)
        arr = insert(arr, idx, val, axis=0)
    return arr

tp = loadtxt('sites_sd', '4a, 3f')
sd_arr = asarray([ii[1] for ii in tp])

ep_obj =  EpochalData('sites_sd_seafloor.h5')
for epoch in range(0,1200):
    arr = invert_seafloor_sd(sd_arr, epoch)
    ep_obj.set_epoch_value(epoch, arr.reshape([-1,1]))

ep_obj.set_info('sites',[ii.encode() for ii in sites_with_seafloor])

