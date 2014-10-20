import viscojapan as vj

G0 = '../G0_He50km_VisK5.0E17_VisM1.0E19_Rake90.h5'
G1 = '../G1_He50km_VisK6.0E17_VisM1.0E19_Rake90.h5'
G2 = '../G2_He50km_VisK5.0E17_VisM2.0E19_Rake90.h5'

G0_ = '../../../../inversion6/occam/iter2/green_function/G_He50km_Vis2.8E19_Rake90.h5'

epoch = 1200
scale = 1e-3
mth = 0
bm = vj.plots.MyBasemap(region_code='near')

mplt = vj.plots.MapPlotDisplacement(bm)
#mplt.plot_G_file_vis(G0,epoch,mth=mth, color='black', scale=scale)
mplt.plot_G_file_vis(G2,epoch,mth=mth, color='red', scale=scale)
vj.plots.plt.show()
