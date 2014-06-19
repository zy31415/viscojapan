from .plot_utils import Map
from ..epochal_data import EpochalIncrSlip

class PlotIncrSlip(object):
    def __init__(self):
        self.map = Map()
        self.map.init()

    def __call__(self, f_slip, epoch):
        slip_obj = EpochalIncrSlip(f_slip)
        slip = slip_obj(epoch)

        self.map.plot_fslip(slip)
        
        
        
