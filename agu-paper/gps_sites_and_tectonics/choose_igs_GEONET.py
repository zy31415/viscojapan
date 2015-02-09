import numpy as np

sites_igs = np.loadtxt('igs.gmt', '4a',usecols=(2,))
sites_all = np.loadtxt('sites_with_seafloor', '4a', usecols=(0,))

sites_GEONET = []

for site in sites_all:
    if site not in sites_igs:
        sites_GEONET.append(site)

import viscojapan as vj

sites_GEONET = [site.decode() for site in sites_GEONET]

vj.sites_db.SitesDB().gets(sites_GEONET).save_to_txt('sites_GEONET.gmt',
                                                   cols = 'lon lat id')
