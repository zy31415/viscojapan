from numpy import loadtxt

from viscojapan.epochal_data import EpochalDisplacementSD

ep = EpochalDisplacementSD('sites_sd.h5','sites_with_seafloor')

seafloor = loadtxt('seafloor_sd', '4a,i, 3f')

for ii in seafloor:
    site = ii[0].decode()
    day = ii[1]
    sd = ii[2]
    print(site, day, sd)

    ep.set_value_at_site(site, 'e', day, sd[0])
    ep.set_value_at_site(site, 'n', day, sd[1])
    ep.set_value_at_site(site, 'u', day, sd[2])
