import numpy as np

import viscojapan as vj

def load_lons_lats():
    tp = np.loadtxt('../stations_large_scale.in', '4a,f,f')
    lons = [ii[1] for ii in tp]
    lats = [ii[2] for ii in tp]
    return lons, lats

lons, lats = load_lons_lats()

epochs = range(0,1344,20)

reader = vj.inv.DeformPartitionResultReader(
    '../../deformation_partition_large_scale.h5')

Ecumu = reader.Ecumu

cmpt = 'Raslip'

obj = getattr(reader, cmpt)
for epoch in epochs:
    print(cmpt, epoch)
    if epoch == 0:
        mags = obj.get_coseismic_disp_hor_mag()
    else:
        mags = obj.get_post_hor_mag_at_epoch(epoch)
    plt = vj.displacement.plot.MagnitudeContoursPlotter()
    plt.plot(lons, lats, mags,
             'plots/%s_day%04d.pdf'%(cmpt,epoch),
             if_topo = False
             )
