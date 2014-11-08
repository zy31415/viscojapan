import viscojapan as vj
import numpy as np

reader = vj.EpochalFileReader('../../tsana/post_fit/cumu_post.h5')
co_disp = reader[0].reshape([-1,3])
sites = np.asarray([ii.decode() for ii in reader['sites']])

obs_dic = {k:v for k, v in zip(sites, co_disp)}


sorted_ver = sorted(obs_dic.items(), key=lambda x: x[1][2])
sorted_hor = sorted(obs_dic.items(),
                    key=lambda x: np.sqrt(x[1][0]**2+x[1][1]**2),
                    reverse = True)
