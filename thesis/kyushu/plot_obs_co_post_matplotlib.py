import viscojapan as vj

with vj.EpochalSitesFileReader(
    '../../tsana/post_fit/cumu_post_with_seafloor.h5') as reader:
    sites = reader.all_sites
    co_disp = reader[0]
    post_disp = reader[1344] - co_disp


bm = vj.plots.MyBasemap(
    region_box = (129.3, 31, 132.1, 33.9),
    resolution = 'i',
    x_interval = 1,
    y_interval = 1
    )

scale = 0.4
U = 3
font_size = 8

mplt = vj.plots.MapPlotDisplacement(bm)

mplt.plot_disp(co_disp, sites, scale=scale, color='black',
               X=0.13, Y=0.04,
               U=0.01*U, label='%d cm co. obs.'%U,
               font_size = font_size)
mplt.plot_disp(post_disp, sites, scale=scale, color='red',
               X=0.13, Y=0.14,
               U=0.01*U, label='%d cm post. obs.'%U,
               font_size = font_size)
# mplt.plot_sites(sites, offset_X=0, offset_Y=-0.05)

vj.plots.plt.savefig('compare_co_post_disp_Kyushu.pdf')
vj.plots.plt.show()
