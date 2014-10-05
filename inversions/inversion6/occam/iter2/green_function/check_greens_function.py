from pylab import plt
import numpy as np

import viscojapan as vj


model0 = 'G_He50km_Vis2.8E19_Rake90.h5'
model1 = 'G_He50km_Vis4.0E19_Rake90.h5'
model2 = 'G_He45km_Vis2.8E19_Rake90.h5'
model3 = 'G_He50km_Vis2.8E19_Rake85.h5'

scale = 1e-4

sites = np.loadtxt('sites_near_field', '4a', usecols=(0,))

bm = vj.MyBasemap(region_code='near')

mplt = vj.MapPlotDisplacement(basemap=bm)

mplt.plot_G_file_vis(model0 , epoch=1000, mth=10,
                      color='red', scale=scale, sites=sites)

mplt.plot_G_file_vis(model2 , epoch=1000, mth=10,
                      color='black', scale=scale, sites=sites)

##mplt.plot_G_file_vis('../../iter1/green_function/G_He50km_Vis5.8E18_Rake90.h5', epoch=1000, mth=10,
##                      color='green', scale=scale, sites=sites)

plt.show()


