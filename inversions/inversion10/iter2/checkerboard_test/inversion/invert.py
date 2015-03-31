from numpy import logspace

import viscojapan as vj

dip_patch_size = 3
strike_patch_size = 4

fault_file = '../../fault_model/fault_bott80km.h5'

rough = vj.inv.reg.Roughening.create_from_fault_file(fault_file)

basis = vj.inv.basis.BasisMatrix.create_from_fault_file(fault_file)

inv = vj.inv.StaticInversion(
    file_G = '../../green_function/G0_He50km_VisM6.3E18_Rake83.h5',
    file_d = '../true_model/d_simu_dip%d_stk%d.h5'%(dip_patch_size, strike_patch_size),
    file_sd = '../sites_sd/sd_uniform.h5',
    filter_sites_file = 'sites_with_seafloor',
    regularization = None,
    fault_file = fault_file,
    basis = basis,
    )

inv.set_data_except_L()

for nth, alpha in enumerate(logspace(-3, 1, 20)):
    reg = vj.inv.reg.Composite().add_component(component = rough,
                                    arg = alpha,
                                    arg_name = 'roughening')
    inv.regularization = reg
    inv.set_data_L()
    inv.invert()
    inv.predict()
    inv.save('outs/dip%d_stk%d_ano_%02d.h5'%\
             (dip_patch_size, strike_patch_size,nth), overwrite=True)


