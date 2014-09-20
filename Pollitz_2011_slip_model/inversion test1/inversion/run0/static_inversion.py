from numpy import logspace
import numpy as np

import viscojapan as vj
from viscojapan.inversion.basis_function import BasisMatrix
from viscojapan.inversion.regularization import Roughening, Composite, \
     NorthBoundary, SouthBoundary, FaultTopBoundary
from viscojapan.inversion.static_inversion import StaticInversion


fault_file = '../../fault_model/fault_bott50km.h5'

rough = Roughening.create_from_fault_file(fault_file)
damping = vj.Intensity.create_from_fault_file(fault_file)
reg_north = NorthBoundary.create_from_fault_file(fault_file)
reg_south = SouthBoundary.create_from_fault_file(fault_file)
reg_top = FaultTopBoundary.create_from_fault_file(fault_file)

basis = BasisMatrix.create_from_fault_file(fault_file)


inv = StaticInversion(
    file_G = '../../greens_function/G_He63km_Rake81.h5',
    file_d = '../cumu_post_with_seafloor.h5',
    file_sd = '../sd/sd_ozawa.h5',
    file_sites_filter = '../sites_with_seafloor',
    regularization = None,
    basis = basis,
)
inv.set_data_except(excepts=['L'])

edge_pars = np.logspace(-3,1,10)

damps = logspace(-3, 1, 30)
roughs = logspace(-3, 1, 30)
for ndamp in range(len(damps)):
    for nrough in range(len(roughs)):
        outf = 'outs/ndamp_%02d_rough_%02d.h5'%(ndamp, nrough)
        print(outf)
        
        reg = Composite().\
              add_component(component = reg_north,
                            arg = 1e5,
                            arg_name = 'north').\
              add_component(component = reg_south,
                            arg = 1e5,
                            arg_name = 'south').\
              add_component(component = rough,
                            arg = roughs[nrough],
                            arg_name = 'roughening').\
              add_component(component = damping,
                            arg = damps[ndamp],
                            arg_name = 'damping').\
              add_component(component = reg_top,
                            arg = 0.01,
                            arg_name = 'top')
        
        inv.regularization = reg
        inv.set_data_L()
        inv.invert()
        inv.predict()
        
        inv.save(outf, overwrite=True)
