import viscojapan as vj


def create_co_aslip_boundary_regularization(
    fault_file, num_epochs,
    co, aslip, boundary):

    rough = vj.inv.reg.Roughening.create_from_fault_file(fault_file)
    co_reg = vj.inv.reg.RegularizationForOnlyFirstEpoch(
        reg = rough,
        num_epochs = num_epochs)

    intensity = vj.inv.reg.Intensity.create_from_fault_file(fault_file)
    aslip_reg = vj.inv.reg.RegularizationExceptFirstEpoch(
        reg = intensity,
        num_epochs = num_epochs)    

    bd = vj.inv.reg.BoundaryRegDeadNorthAndSouth.\
         create_from_fault_file(fault_file)
    boundary_reg = vj.inv.reg.ExpandForAllEpochs(
        reg = bd,
        num_epochs = num_epochs)

    reg = vj.inv.reg.Composite().\
          add_component(co_reg, arg=co, arg_name='coseismic'). \
          add_component(aslip_reg, arg=aslip, arg_name='aslip'). \
          add_component(boundary_reg, arg=boundary, arg_name='boundary')

    return reg
