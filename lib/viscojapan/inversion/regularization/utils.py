from .regularization import Composite
from .roughening import Roughening, ExpandForAllEpochs
from .temporal_regularization import TemporalRegularization
from .intensity import Intensity

def create_roughening_temporal_regularization(
    fault_file, epochs, rough, temp):

    reg_rough = Roughening.create_from_fault_file(fault_file)
    expanded_reg = ExpandForAllEpochs(reg = reg_rough, num_epochs = len(epochs))

    reg_temp = TemporalRegularization.create_from_fault_file(fault_file, epochs)
    
    reg = Composite().\
          add_component(expanded_reg, arg=rough, arg_name='roughening').\
          add_component(reg_temp, arg=temp, arg_name='temporal')
    
    return reg

##def create_roughening_temporal_intensity_regularization(
##    fault_file, epochs, rough, temp, intensity):
##
##    reg_rough = Roughening.create_from_fault_file(fault_file)
##    exp_reg_rough = ExpandForAllEpochs(reg = reg_rough, num_epochs = len(epochs))
##
##    reg_temp = TemporalRegularization.create_from_fault_file(fault_file, epochs)
##
##    reg_intensity = Intensity.create_from_fault_file(fault_file)
##    exp_reg_inten = ExpandForAllEpochs(reg = reg_intensity, num_epochs = len(epochs))
##    
##    reg = Composite().\
##          add_component(exp_reg_rough, arg=rough, arg_name='roughening').\
##          add_component(reg_temp, arg=temp, arg_name='temporal').\
##          add_component(exp_reg_inten, arg=intensity, arg_name='intensity')
##    
##    return reg

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
