import viscojapan as vj
from pylab import plt

res_file = '../../outs/nco_06_naslip_10.h5'
disp_obs_file = '../../../obs/cumu_post_with_seafloor.h5'
epoch = 1100

scale = 16.
X = 0.1
Y = 0.8
U = 1.
label_pred = '%.1f m pred.'%U
label_obs = '%.1f m obs.'%U

bm = vj.plots.MyBasemap(
    region_code='near')

# prediction
reader = vj.inv.ResultFileReader(res_file)
sites = reader.sites
disp = reader.get_post_disp_at_epoch(epoch)

mplt = vj.plots.MapPlotDisplacement(bm)
mplt.plot_disp(disp, sites, color='red',
               X = X, Y = Y, U=U, label=label_pred,
               scale = scale)

# observation:
reader = vj.EpochalFileReader(disp_obs_file)
dips_obs = reader[epoch] - reader[0]
sites_obs = [site.decode() for site in reader['sites']]
mplt = vj.plots.MapPlotDisplacement(bm)
mplt.plot_disp(dips_obs, sites_obs, color='black',
               X = X, Y = Y+0.1, U=U, label=label_obs,
               scale = scale)

# trench:
mplt = vj.plots.MapPlotSlab()
mplt.plot_top()

plt.title('Postseismic disp. (1100 days) pred. vs. obs.')

plt.savefig('post_seismic_disp.pdf')
plt.show()

