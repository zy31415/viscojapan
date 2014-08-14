from numpy import logspace
import numpy as np

from viscojapan.inversion.basis_function import BasisMatrix
from viscojapan.inversion.regularization import Roughening, Composite, \
     PunishEdge
from viscojapan.inversion.static_inversion import StaticInversion


fault_file = 'fault_bott40km.h5'

rough = Roughening.create_from_fault_file(fault_file)
edge = PunishEdge.create_from_fault_file(fault_file)

basis = BasisMatrix.create_from_fault_file(fault_file)


inv = StaticInversion(
    file_G = 'G_He40km_Vis1.1E19_Rake81.h5',
    file_d = 'cumu_post_with_seafloor.h5',
    file_sd = './sd_seafloor/sd_with_seafloor.h5',
    file_sites_filter = 'sites_with_seafloor',
    regularization = None,
    basis = basis,
)
inv.set_data_except_L()

edge_pars = np.logspace(-3,1,10)

for nth, alpha in enumerate(logspace(-3, 1, 30)):
    for nedg, edge_par in enumerate(edge_pars):
        reg = Composite().\
              add_component(component = rough,
                            arg = alpha,
                            arg_name = 'roughening').\
              add_component(component = edge,
                            arg = edge_par,
                            arg_name = 'edging')
        
        inv.regularization = reg
        inv.set_data_L()
        inv.invert()
        inv.predict()
        inv.save('outs/ano_%02d_edg_%02d.h5'%(nth,nedg), overwrite=True)
