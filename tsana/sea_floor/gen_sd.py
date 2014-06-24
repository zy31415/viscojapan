from numpy import loadtxt, mean

from tenv_file_reader.tenv_file_reader import read_tenv_tssd

sites = loadtxt('sites','4a')
sites_with_seafloor = loadtxt('sites_with_seafloor','4a')

fid = open('sites_with_seafloor_sd','wt')
fid.write('# site mean(esd) mean(nsd) mean(usd)\n')
for site in sites_with_seafloor:
    print(site.decode())
    if site in sites:
        esd = read_tenv_tssd('../raw_ts/IGS08/%s.IGS08.tenv'%site.decode(),'e')
        nsd = read_tenv_tssd('../raw_ts/IGS08/%s.IGS08.tenv'%site.decode(),'n')
        usd = read_tenv_tssd('../raw_ts/IGS08/%s.IGS08.tenv'%site.decode(),'u')

        esd_m = mean(esd)
        nsd_m = mean(nsd)
        usd_m = mean(usd)
    else:
        esd_m = 0.5
        nsd_m = 0.5
        usd_m = 0.5

    fid.write('%s  %f  %f  %f\n'%(site.decode(), esd_m, nsd_m, usd_m))

fid.close()
