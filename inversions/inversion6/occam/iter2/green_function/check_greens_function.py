from pylab import plt

import viscojapan as vj


model0 = 'G_He50km_Vis2.8E19_Rake90.h5'
model2 = 'G_He45km_Vis2.8E19_Rake90.h5'
model3 = 'G_He50km_Vis2.8E19_Rake85.h5'

scale = 1e-4

bm = vj.MyBasemap(region_code='near')

mplt = vj.MapPlotDisplacement(basemap=bm)

mplt.plot_G_file_vis(model0 , epoch=1000, mth=10,
                      color='black', scale=scale)

mplt.plot_G_file_vis(model2 , epoch=1000, mth=10,
                      color='red', scale=scale)

plt.show()


