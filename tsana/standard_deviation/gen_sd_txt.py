from numpy import loadtxt, mean

from tenv_file_reader.tenv_file_reader import read_tenv_tssd

sites = loadtxt('sites','4a')

with open('sites_sd','wt') as fid:
    fid.write('# site mean(esd) mean(nsd) mean(usd)\n')
    for site in sites:
        print(site.decode())
        esd = read_tenv_tssd('../raw_ts/IGS08/%s.IGS08.tenv'%site.decode(),'e')
        nsd = read_tenv_tssd('../raw_ts/IGS08/%s.IGS08.tenv'%site.decode(),'n')
        usd = read_tenv_tssd('../raw_ts/IGS08/%s.IGS08.tenv'%site.decode(),'u')

        esd_m = mean(esd)
        nsd_m = mean(nsd)
        usd_m = mean(usd)

        fid.write('%s  %f  %f  %f\n'%(site.decode(), esd_m, nsd_m, usd_m))
