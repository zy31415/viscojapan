from numpy import logspace

import viscojapan as vj


fault_file = '../fault_model/fault_He50km.h5'

rough = vj.Roughening.create_from_fault_file(fault_file)

basis = vj.BasisMatrix.create_from_fault_file(fault_file)

inv = vj.StaticInversion(
    file_G = '../greens_function/G_Rake80.h5',
    file_d = '../true_model/d_simu.h5',
    file_sd = '../sites_sd/sites_sd.h5',
    file_sites_filter = 'sites_with_seafloor',
    regularization = None,
    basis = basis,
    )

inv.set_data_except_L()

for nth, alpha in enumerate(logspace(-3, 1, 30)):
    reg = vj.Composite().add_component(component = rough,
                                    arg = alpha,
                                    arg_name = 'roughening')
    inv.regularization = reg
    inv.set_data_L()
    inv.invert()
    inv.predict()
    inv.save('outs/ano_%02d.h5'%nth, overwrite=True)


