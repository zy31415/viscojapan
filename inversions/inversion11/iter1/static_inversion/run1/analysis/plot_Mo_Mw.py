import viscojapan as vj

from epochs import epochs

fault_file = '../../fault_model/fault_bott80km.h5'

earth_file = '../../earth_model_nongravity/He50km_VisM6.3E18/earth.model_He50km_VisM6.3E18'

cal = vj.mo.MomentCalculator(fault_file, earth_file)

for epoch in epochs:
    reader = vj.inv.ResultFileReader('../outs/outs_%04d/rough_%02d.h5'%(epoch, 6))
    if epoch == 0:
        co = reader.m
        s = co
    else:
        s = reader.m - co
    mo, mw = cal.compute_moment(s)
    print(mo, mw)
