import numpy as np

import viscojapan as vj

tp = np.loadtxt('../pre_vel', '4a,2f,3f,3f')
sites = [ii[0] for ii in tp]

d = np.asarray([ii[2] for ii in tp]).flatten()

scale = 9e2

bm = vj.plots.MyBasemap(
    region_box = (128,29,146,46),
    x_interval = 5,
    y_interval = 5)

mplt = vj.plots.MapPlotSlab(basemap=bm)
mplt.plot_top()

vj.plots.plot_epicenter(bm)

mplt = vj.plots.MapPlotDisplacement(basemap=bm)
mplt.plot_disp(d, sites, scale=scale,
               X=0.25, Y=0.85,
               U=30., label='30. mm/yr', color='red')

vj.plots.plt.savefig('GEONET_pre_vel.pdf')
vj.plots.plt.show()
