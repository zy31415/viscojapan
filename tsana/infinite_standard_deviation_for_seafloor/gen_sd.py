from numpy import loadtxt, mean, asarray

from tenv_file_reader.tenv_file_reader import read_tenv_tssd
from viscojapan.epochal_data import EpochalData

sites_with_seafloor = loadtxt('sites_with_seafloor','4a')
tp = loadtxt('sites','4a')
sites = [ii.decode() for ii in tp]

with open('sites_sd','wt') as fid:
    fid.write('# site mean(esd) mean(nsd) mean(usd)\n')
    for site in sites_with_seafloor:
        site = site.decode()
        print(site)
        if site in sites:
            esd = read_tenv_tssd('../raw_ts/IGS08/%s.IGS08.tenv'%site,'e')
            nsd = read_tenv_tssd('../raw_ts/IGS08/%s.IGS08.tenv'%site,'n')
            usd = read_tenv_tssd('../raw_ts/IGS08/%s.IGS08.tenv'%site,'u')

            esd_m = mean(esd)
            nsd_m = mean(nsd)
            usd_m = mean(usd)

            fid.write('%s  %f  %f  %f\n'%(site, esd_m, nsd_m, usd_m))
        else:
            fid.write('%s  +inf  +inf  +inf\n'%site)

tp = loadtxt('sites_sd', '4a, 3f')
sd_arr = asarray([ii[1] for ii in tp], float)

ep_obj =  EpochalData('sites_sd.h5')
for epoch in range(0,1200):    
    ep_obj.set_epoch_value(epoch, sd_arr.reshape([-1,1]))

ep_obj.set_info('sites',[ii for ii in sites_with_seafloor])
    
