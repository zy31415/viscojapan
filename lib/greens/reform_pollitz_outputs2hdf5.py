from os.path import join

from numpy import NaN

class ReformPollitzOutputs2HDF5(object):
    ''' This class reform the original outputs by STATIC1D & VISCO1D
into a HDF5 file.
'''
    def __init__(self):
        self.days_of_epochs = []
        self.no_of_subfaults = NaN
        self.obs_sites = []

        self.pollitz_outputs_dir = ""
        self.output_filename_hdf5 = ""

        self.He = NaN
        self.visM = NaN
        self.visK = NaN
        self.lmax = NaN

    def _check_pollitz_outputs_existence(self):
        for day in self.days_of_epochs:
            for fltno in range(0, self.no_of_subfaults):
                fn1 = 'day%04d#flt%04d'%(day,fltno)
                fn2 = join(self.pollitz_outputs_dir, fn1)
                assert exists(fn2), "File %s is not exists! Abort."%fn2
        
        
        
