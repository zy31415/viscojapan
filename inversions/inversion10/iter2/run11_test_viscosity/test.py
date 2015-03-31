import numpy as np
from pylab import plt

import viscojapan as vj

sites = vj.utils.as_string(np.loadtxt('sites_with_seafloor', '4a', usecols=(0,)))

ed1 = vj.inv.ep.EpochG('../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
                       mask_sites = sites)

ed2 = vj.inv.ep.EpochG('../green_function/G1_He50km_VisM1.0E19_Rake83.h5',
                       mask_sites = sites)

diffG = vj.inv.ep.DifferentialG(ed1, ed2, 'log10(visM)')

vis = 8.9E18

epoch = 1344

dG = diffG.get_data_at_epoch(epoch)

reader = vj.inv.ResultFileReader('../run11/outs/best_result.h5')
slip = reader.get_slip()
disp = reader.get_obs_disp()

obs_disp = disp.get_post_at_epoch(epoch)

co_slip = slip.get_coseismic_slip()


d = np.dot((ed1[epoch] - ed1[0])+dG*(np.log10(vis) - diffG.var1),
           co_slip.reshape([-1,1]))

scale = 10
U = 1.
region_code = 'A'
bm = vj.plots.MyBasemap(region_code=region_code)

mplt = vj.plots.MapPlotDisplacement(bm)
mplt.plot_disp(d, sites,
               scale = scale,
               label = 'Rco 1m',
               Y = 0.7,
               U = U,
               )

mplt.plot_disp(obs_disp.flatten(), sites,
               color = 'red',
               scale = scale,
               label = 'obs. 1m',
               Y = 0.8,
               U = U
               )
plt.savefig('%s.png'%region_code)
plt.show()
