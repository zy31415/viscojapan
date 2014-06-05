from numpy import asarray

from .slip import EpochalIncrSlip, EpochalSlip

class FormSlip(object):
    def __init__(self):
        self.solution = None
        self.epochs = None
        self.nlin_par_names = []

        self.num_of_subfaults = 250

    def init(self):
        self.num_of_nlin_pars = len(self.nlin_par_names)
        self.incr_slip_arr = asarray(self.solution['x'])[0:-self.num_of_nlin_pars]
        self.nlin_par_vals = asarray(self.solution['x'])[-self.num_of_nlin_pars:]
        self.nlin_par_vals = self.nlin_par_vals.flatten()
        
        for pn, val in zip(self.nlin_par_names,
                           self.nlin_par_vals):
            setattr(self,pn,val)

    def gen_inverted_incr_slip_file(self, incr_slip_file, info_dic={}):
        incr_slip = EpochalIncrSlip(incr_slip_file)
        for nth, epoch in enumerate(self.epochs):
            incr_slip.set_epoch_value(epoch,self.incr_slip_arr[
                nth*self.num_of_subfaults:(nth+1)*self.num_of_subfaults, 0])

        incr_slip.set_info('incr_slip_arr', self.incr_slip_arr)
        incr_slip.set_info('num_of_subfaults', self.num_of_subfaults)
        
        for par in self.nlin_par_names:
            incr_slip.set_info(par, getattr(self,par))
        incr_slip.set_info_dic(info_dic)

    def gen_inverted_slip_file(self, slip_file):
        slip = EpochalSlip(slip_file)
        for nth, epoch in enumerate(self.epochs):
            if nth == 0:
                val0 = self.incr_slip_arr[nth*self.num_of_subfaults:
                                          (nth+1)*self.num_of_subfaults,0]
            else:
                val = self.incr_slip_arr[nth*self.num_of_subfaults:
                                         (nth+1)*self.num_of_subfaults,0]
                val0 += val
            slip.set_epoch_value(epoch,val0)

