import viscojapan as vj

import numpy as np

reader = vj.EpochalFileReader('G.h5')
G = reader[0]


res_file = '../run2_seafloor_01/outs/nrough_14_ntop_02.h5'
fault_file = '../../fault_model/fault_bott60km.h5'
reader = vj.ResultFileReader(res_file)
slip = reader.slip

d_pred = np.dot(G,slip).reshape([-1,3])

sites = np.loadtxt('sites.in', '4a, f, f')

_txt = np.array([(s[1], s[2], d[0], d[1], s[0]) for s, d in zip(sites, d_pred)],
                ('f, f, f, f, U4'))
np.savetxt('pred_disp',_txt, fmt='%f %f %f %f %s')


_txt = np.array([(s[1], s[2], np.sqrt(d[0]**2+d[1]**2), s[0]) for s, d in zip(sites, d_pred)],
                ('f, f, f, U4'))
np.savetxt('pred_disp_mag',_txt, fmt='%f %f %f %s')
