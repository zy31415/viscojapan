import numpy as np

import viscojapan as vj

sites = np.loadtxt('sites_with_seafloor','4a')
sites_far_field = np.loadtxt('sites_far_field','4a')

bm = vj.MyBasemap(
    region_code = 'all',
    )
mplt = vj.MapPlotDisplacement(basemap=bm)
mplt.plot_sites(sites, marker='.', color='blue')
mplt.plot_sites(sites_far_field,color='red')

vj.plot_regions_on_basemap(bm)
vj.plt.savefig('regions_and_far_field_sites.png')
vj.plt.show()
vj.plt.close()
