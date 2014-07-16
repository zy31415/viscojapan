from .regularization import Composite
from .roughening import Roughening, ExpandForAllEpochs
from .temporal_regularization import TemporalRegularization

def create_roughening_temporal_regularization(
    fault_file, epochs, rough, temp):

    reg_rough = Roughening.create_from_fault_file(fault_file)
    expanded_reg = ExpandForAllEpochs(reg = reg_rough, num_epochs = len(epochs))

    reg_temp = TemporalRegularization.create_from_fault_file(fault_file, epochs)
    
    reg = Composite().\
          add_component(expanded_reg, arg=rough, arg_name='roughening').\
          add_component(reg_temp, arg=temp, arg_name='temporal')
    
    return reg
