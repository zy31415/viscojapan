import numpy as np

import viscojapan as vj


ep = vj.EpochalDisplacement('../../cumu_post.h5')

co = ep[0]
disp = ep[1200] - co
sites = ep.get_sites

sites_7_2EXPs = vj.tsana.get_sites_according_to_postmodel('../../../config/postmodel',7,'2EXPs')
sites_6_2EXPs = vj.tsana.get_sites_according_to_postmodel('../../../config/postmodel',6,'2EXPs')
sites_7_EXP = vj.tsana.get_sites_according_to_postmodel('../../../config/postmodel',7,'EXP')
sites_6_EXP = vj.tsana.get_sites_according_to_postmodel('../../../config/postmodel',6,'EXP')

##
scale = 1.7
U = 0.1

bm = vj.plots.MyBasemap(
    region_code = 'H',
    #region_box = (128,29,146,46),
    x_interval = 2,
    y_interval = 2)

mplt = vj.plots.MapPlotSlab(basemap=bm)
mplt.plot_top()

vj.plots.plot_epicenter(bm)

mplt = vj.plots.MapPlotDisplacement(basemap=bm)

mplt.plot_disp(disp, sites, sites_subset=sites_7_2EXPs, scale=scale,
               X=0.2, Y=0.85,
               U=U, label='%.1f m - Based on Model 2EXPs'%U, color='red',
               font_size=8)

mplt.plot_disp(disp, sites, sites_subset=sites_7_EXP, scale=scale,
               X=0.2, Y=0.77,
               U=U, label='%.1f m - Based on Model EXP'%U, color='black',
               font_size=8)

vj.plots.plt.savefig('post_disp_region_H__day_1200.pdf')
vj.plots.plt.show()
