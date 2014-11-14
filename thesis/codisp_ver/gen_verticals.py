import numpy as np

import viscojapan as vj

reader = vj.EpochalFileReader('../../tsana/post_fit/cumu_post.h5')
co_disp = reader[0].reshape([-1,3])
sites = vj.Sites([ii.decode() for ii in reader['sites']])


_txt = np.array([(site.lon, site.lat, abs(ci[2]), site.name)
                 for ci, site in zip(co_disp, sites)],
                ("f,f,f,U4")
                )
np.savetxt('verticals_abs', _txt, '%f %f %f %s')


_txt = np.array([(site.lon, site.lat, ci[2], site.name)
                 for ci, site in zip(co_disp, sites)],
                ("f,f,f,U4")
                )
np.savetxt('verticals', _txt, '%f %f %f %s')
