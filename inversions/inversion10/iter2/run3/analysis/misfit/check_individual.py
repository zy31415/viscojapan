from pylab import plt

import viscojapan as vj

res_file = '../../outs/nrough_06_naslip_11.h5'

ana = vj.inv.DispAnalyser(res_file)

obs = ana.get_cumu_obs_3d()
pred = ana.get_cumu_pred_3d()

sites = ana.result_file_reader.sites
epochs = ana.result_file_reader.epochs

site = 'G162'

idx = sites.index(site)

y_obs = obs[:,idx,0]
y_pred = pred[:,idx,0]

reader = vj.EpochalSitesFileReader('../../../obs/cumu_post_with_seafloor.h5')

y_obs1 = []
for epoch in epochs:
    y_obs1.append(reader.get_epoch_value_at_site(site, 'e', epoch))

plt.plot(epochs, y_obs, color='blue')
plt.plot(epochs, y_obs1, color='green')
plt.plot(epochs, y_pred, color='red')

plt.show()




