import viscojapan as vj

bm = vj.MyBasemap(region_code = 'all')

sites_file_far_field = 'sites_far_field'
sites_far_field = np.loadtxt(sites_file_far_field, '4a')

sites_file = '../../sites_with_seafloor'
sites = np.loadtxt(sites_file, '4a')

res_file = '../outs/nsd_03_rough_10_top_02.h5'

d_obs = vj.EpochalDisplacement('../../cumu_post_with_seafloor.h5',
                               sites_file_far_field)[0]

with h5py.File(res_file,'r') as fid:
    Bm = fid['Bm'][...]
    d_pred = fid['d_pred'][...]

pltd = PlotCoseismicDisp(
    d_obs =  d_obs,
    d_pred = d_pred,
    sites = sites,
    )
pltd.plot_at_all()
plt.savefig('plots_disp/far_field.png')
plt.close()
