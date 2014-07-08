from os.path import join, exists

from numpy import NaN, loadtxt, asarray

from .epochal_data import EpochalData

class PollitzOutputsToEpochalData(EpochalData):
    ''' This class reform the original outputs by STATIC1D & VISCO1D
into a HDF5 file. Provide necessary information about green functions.
Use extra_info and extra_info_attr to add more information about the
green's function: These properties are highly recommended:

        He : elastic thickness
        visM : Maxwellian viscosity
        visK : Kelvin viscosity
        lmax_VISCO1D : lmax used in VISCO1D

    etc.
'''
    def __init__(self, epoch_file):
        super().__init__(epoch_file)

        # initialize the following variables!
        self.days_of_epochs = []
        self.no_of_subfaults = NaN
        self.pollitz_outputs_dir = ""        
        self.file_stations_in = ""

        self.extra_info = {}
        self.extra_info_attrs = {}


    def _assert_initialization(self):
        assert len(self.days_of_epochs) != 0, "Have you initialize the object?"
        assert self.no_of_subfaults != NaN, "Have you initialize the object?"
        assert self.pollitz_outputs_dir != "", "Have you initialize the object?"
        assert self.epoch_file != "", "Have you initialize the object?"
        assert self.file_stations_in != ""
        
    def _check_pollitz_outputs_existence(self):
        for day in self.days_of_epochs:
            for fltno in range(0, self.no_of_subfaults):
                fn = self._form_file_name(day, fltno)
                assert exists(fn), "File %s is not exists! Abort."%fn

    def _check_hdf5_existence(self):
        assert not exists(self.epoch_file), \
               "Output HDF5 already exists!"

    def _form_file_name(self, day, fltno):
        fn1 = 'day%04d#flt%04d'%(day,fltno)
        fn2 = join(self.pollitz_outputs_dir, fn1)
        return fn2

    
    def _read_a_day(self, day):        
        read_file = lambda fn : loadtxt(fn)[:,2:5].flatten()
        
        G=[]
        for fltno in range(0, self.no_of_subfaults):
            fn = self._form_file_name(day, fltno)
            col = read_file(fn)
            G.append(col)
        G=asarray(G).transpose()
        return G

    def _write_G_to_hdf5(self):    
        for day in self.days_of_epochs:
            print(day)
            G = self._read_a_day(day)
            if day == 0:
                self.set_epoch_value(0, G)
            else:
                G0 = self.get_epoch_value(0)
                self.set_epoch_value(day, G + G0)

    def _get_sites(self):
        tp = loadtxt(self.file_stations_in,'2f,4a')
        sites = [ii[1] for ii in tp]
        return sites

    def _write_info_to_hdf5(self):
        self.set_info('sites', self._get_sites())
        self.set_info('no_of_subfaults', self.no_of_subfaults)

    def _write_extra_info_to_hdf5(self):        
        for key, value in self.extra_info.items():
            self.set_info(key,value)
        for key, attrs in self.extra_info_attrs.items():
            for key_attr, value_attr in attrs.items():
                self.set_info_attr(key, key_attr, value_attr)

    def __call__(self):
        self._assert_initialization()
        self._check_pollitz_outputs_existence()
        self._check_hdf5_existence()
        self._write_G_to_hdf5()
        self._write_info_to_hdf5()
        self._write_extra_info_to_hdf5()

    
            
        

    



     
        
        
