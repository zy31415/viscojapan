import numpy as np

import viscojapan as vj

reader = vj.inv.ResultFileReader('../run11/outs/best_result.h5')

slip = reader.get_slip()
co_slip = slip.get_coseismic_slip()

obs_disp = reader.get_obs_disp()

pred_disp = reader.get_pred_disp()

epoch = 1344
d_obs = obs_disp.get_post_at_epoch(epoch)
d_pred = pred_disp.get_post_at_epoch(epoch)

sites = vj.utils.as_string(np.loadtxt('sites_with_seafloor', '4a', usecols=(0,)))

ed1 = vj.inv.ep.EpochG('../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
                       mask_sites = sites)

ed2 = vj.inv.ep.EpochG('../green_function/G1_He50km_VisM1.0E19_Rake83.h5',
                       mask_sites = sites)

diffG = vj.inv.ep.DifferentialG(ed1, ed2, 'log10(visM)')

vis = 1E17

dG = diffG.get_data_at_epoch(epoch)

dd = np.dot(dG*(np.log10(vis) - diffG.var1),
           co_slip.reshape([-1,1]))

res = d_obs - d_pred - dd.reshape([-1,3])

print(np.sqrt(np.mean(res.flatten()**2)))
