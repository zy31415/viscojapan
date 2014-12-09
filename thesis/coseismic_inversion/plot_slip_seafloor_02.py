from os.path import join

import viscojapan as vj


# plot slip
base_dir = '/home/zy/workspace/viscojapan/inversions/static_inversion/static_inversion2'
res_file = join(
    base_dir,
    'coseismic/run2_seafloor_01/outs/nrough_14_ntop_02.h5')
fault_file = join(
    base_dir,
    'fault_model/fault_bott60km.h5')
earth_file = join(
    base_dir,
    'earth_model_nongravity/He63km_VisM1.0E19/earth.model_He63km_VisM1.0E19')

plt = vj.gmt.SlipAtOneEpochPlotter(
    res_file,
    fault_file,
    earth_file
    )

plt.plot('inverted_coseismic_slip_seafloor_02.pdf')
plt.clean()
