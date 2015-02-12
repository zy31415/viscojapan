from .regularization import Composite
from .roughening import Roughening
from .expand_for_epochs import ExpandForAllEpochs, \
     ExpandForOnlyFirstEpoch, ExpandExceptFirstEpoch, ExpandForCumulativeSlip
from .temporal_regularization import TemporalRegularization
from .intensity import Intensity
from .boundary import BoundaryRegDeadNorthAndSouth

__all__ = ['create_roughening_temporal_regularization',
           'create_temporal_damping_roughening_regularization',
           'create_co_aslip_boundary_regularization',
           'create_temporal_edge_roughening',
           'create_rough_aslip_boundary_regularization',
           'create_CumuRough_Edge_Temp_regularization'
           ]

def create_roughening_temporal_regularization(
    fault_file, epochs, rough, temp):

    reg_rough = Roughening.create_from_fault_file(fault_file)
    expanded_reg = ExpandForAllEpochs(reg = reg_rough, num_epochs = len(epochs))

    reg_temp = TemporalRegularization.create_from_fault_file(fault_file, epochs)
    
    reg = Composite().\
          add_component(expanded_reg, arg=rough, arg_name='roughening').\
          add_component(reg_temp, arg=temp, arg_name='temporal')
    
    return reg


def create_temporal_damping_roughening_regularization(
    fault_file, epochs, temp, damp, rough):

    reg_temp = TemporalRegularization.create_from_fault_file(fault_file, epochs)

    reg_intensity = Intensity.create_from_fault_file(fault_file)
    exp_reg_inten = ExpandForAllEpochs(reg = reg_intensity, num_epochs = len(epochs))
    
    reg_rough = Roughening.create_from_fault_file(fault_file)
    exp_reg_rough = ExpandForAllEpochs(reg = reg_rough, num_epochs = len(epochs))
 
    reg = Composite().\
          add_component(reg_temp, arg=temp, arg_name='temporal'). \
          add_component(exp_reg_inten, arg=damp, arg_name='damping'). \
          add_component(exp_reg_rough, arg=rough, arg_name='roughening')
          
    return reg

def create_temporal_edge_roughening(
    fault_file, epochs, temp, edging, rough):
    num_epochs = len(epochs)
    
    reg_temp = TemporalRegularization.create_from_fault_file(fault_file, epochs)

    tp = BoundaryRegDeadNorthAndSouth.create_from_fault_file(fault_file)
    reg_edging = ExpandForAllEpochs(tp, num_epochs)

    tp = Roughening.create_from_fault_file(fault_file)
    reg_rough = ExpandForAllEpochs(reg = tp, num_epochs = num_epochs)

    reg = Composite().\
          add_component(reg_temp, arg=temp, arg_name='temporal'). \
          add_component(reg_edging, arg=edging, arg_name='edging'). \
          add_component(reg_rough, arg=rough, arg_name='roughening')
          
    return reg

def create_co_aslip_boundary_regularization(
    fault_file, num_epochs,
    co, aslip, boundary):

    rough = Roughening.create_from_fault_file(fault_file)
    co_reg = ExpandForOnlyFirstEpoch(
        reg = rough,
        num_epochs = num_epochs)

    intensity = Intensity.create_from_fault_file(fault_file)
    aslip_reg = ExpandExceptFirstEpoch(
        reg = intensity,
        num_epochs = num_epochs)    

    bd = BoundaryRegDeadNorthAndSouth.\
         create_from_fault_file(fault_file)
    boundary_reg = ExpandForAllEpochs(
        reg = bd,
        num_epochs = num_epochs)

    reg = Composite().\
          add_component(co_reg, arg=co, arg_name='coseismic'). \
          add_component(aslip_reg, arg=aslip, arg_name='aslip'). \
          add_component(boundary_reg, arg=boundary, arg_name='boundary')

    return reg

def create_rough_aslip_boundary_regularization(
    fault_file, num_epochs,
    rough, aslip, boundary):

    rough_per_epoch = Roughening.create_from_fault_file(fault_file)
    rough_reg = ExpandForAllEpochs(
        reg = rough_per_epoch,
        num_epochs = num_epochs)

    intensity = Intensity.create_from_fault_file(fault_file)
    aslip_reg = ExpandExceptFirstEpoch(
        reg = intensity,
        num_epochs = num_epochs)    

    bd = BoundaryRegDeadNorthAndSouth.\
         create_from_fault_file(fault_file)
    boundary_reg = ExpandForAllEpochs(
        reg = bd,
        num_epochs = num_epochs)

    reg = Composite().\
          add_component(rough_reg, arg=rough, arg_name='roughness'). \
          add_component(aslip_reg, arg=aslip, arg_name='aslip'). \
          add_component(boundary_reg, arg=boundary, arg_name='boundary')

    return reg   
    

def create_CumuRough_Edge_Temp_regularization(
    fault_file, epochs,
    cumu_rough,
    edge,
    temp
    ):

    num_epochs = len(epochs)
    
    # cumu rough
    tp = Roughening.create_from_fault_file(fault_file)
    reg_cumu_rough = ExpandForCumulativeSlip(reg = tp,
                                           num_epochs = num_epochs)

    # edge
    tp = BoundaryRegDeadNorthAndSouth.create_from_fault_file(fault_file)
    reg_edge = ExpandForAllEpochs(tp, num_epochs)

    # temp
    reg_temp = TemporalRegularization.create_from_fault_file(fault_file, epochs)
    
    
    reg = Composite().\
          add_component(reg_cumu_rough, arg=cumu_rough, arg_name='cumu_rough').\
          add_component(reg_edge, arg=edge, arg_name='edge').\
          add_component(reg_temp, arg=temp, arg_name='temp')
    
    return reg    
