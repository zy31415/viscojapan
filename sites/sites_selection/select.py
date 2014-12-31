import numpy as np

import pGMT 
import viscojapan as vj

sites_2EXPs = [site.decode() for site in np.loadtxt('sites_2EXPs','4a')]

sites_pos = vj.sites_db.get_pos_dic()

py = 42.5, 42.5, 38.83, 35.75, 35.25
px = 143, 137, 136.77, 139.92, 141.11

ch = vj.sites_db.choose_sites_in_polygon(sites_2EXPs, px, py)

sites = list(np.asarray(sites_2EXPs)[ch])

sites_seafloor = list(vj.sites_db.get_pos_dic_of_a_network('SEAFLOOR_POST').keys())

sites += sites_seafloor
sites = sorted(sites)

plt = vj.gmt.SitesPlotter()
plt.plot(sites)
plt.save('sites.pdf')

np.savetxt('sites_Yamagiwa', sites, fmt='%s')
