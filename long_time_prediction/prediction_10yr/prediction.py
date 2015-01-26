import numpy as np

import viscojapan as vj

res_file = '../../inversions/inversion10/iter2/run7/outs/nrough_05_naslip_11.h5'
fault_file = '../fault_model/fault_bott80km.h5'

reader = vj.inv.SlipResultReader(res_file, fault_file)

slip = reader.get_3d_cumu_slip()
slip = slip[-1].reshape([-1, 1])

ep = vj.EpochalG('../green_function_large_scale/G0_He51km_VisM7.9E18_Rake83.h5')
epochs = ep.get_epochs()

G = ep[3650]

disp = np.dot(G, slip).reshape([-1,3])


pos = np.loadtxt('../green_function_large_scale/stations_large_scale.in','4a, f, f')


with open('pred_10yr','wt') as fid:
    for tp, y in zip(pos, disp):
        lon = tp[1]
        lat = tp[2]
        mag = np.sqrt(y[0]**2+y[1]**2)
        fid.write('%f %f %f\n'%(lon, lat, mag))
