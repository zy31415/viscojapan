from numpy import logspace

from viscojapan.inversion.basis_function import BasisMatrix
from viscojapan.inversion.regularization import Roughening, Composite
from viscojapan.inversion.inversion_test.checkerboard_test import \
     StaticInversionTest
from viscojapan.inversion.inversion_test.checkerboard_slip import \
     gen_checkerboard_slip_from_fault_file

fault_file = 'fault_He50km_east.h5'


basis = BasisMatrix.create_from_fault_file(fault_file)

slip = gen_checkerboard_slip_from_fault_file(fault_file, 4, 4).reshape([-1,1])

rough = Roughening.create_from_fault_file(fault_file)

inv = StaticInversionTest(
    file_G = 'G.h5',
    file_sites_filter = 'sites_with_seafloor',
    slip_true = slip,
    sd_horizontal = 6e-3,
    sd_up = 20e03,
    regularization = rough,
    basis = basis
    )
inv.set_data_all()

for nth, alpha in enumerate(logspace(-3, 1, 30)):
    reg = Composite().add_component(component = rough,
                                    arg = alpha,
                                    arg_name = 'roughening')
    inv.regularization = reg
    inv.set_data_L()
    inv.run()
    
    inv.save('outs/ano_%02d.h5'%nth, overwrite=True)
