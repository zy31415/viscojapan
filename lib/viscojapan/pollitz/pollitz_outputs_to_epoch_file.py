from os.path import join, exists

from numpy import NaN, loadtxt, asarray, zeros

from ..epochal_data import EpochalData
from ..utils import delete_if_exists

class PollitzOutputsToEpochalData(object):
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
    def __init__(self,
                 epochs,
                 G_file,
                 num_subflts,
                 pollitz_outputs_dir,
                 sites = None,
                 sites_file = None,
                 G_file_overwrite = True,
                 extra_info = None,
                 extra_info_attrs = None,
                 ):

        # initialize the following variables!
        self.epochs = epochs
        self.num_subflts = num_subflts
        self.pollitz_outputs_dir = pollitz_outputs_dir      

        self.sites = sites
        self.sites_file = sites_file
        
        if self.sites is  not None and self.sites_file is not None:
            raise ValueError('Sites are ambigous.')

        if self.sites is None and self.sites_file is None:
            raise ValueError('No sites are indicated.')

        if self.sites_file is not None:
            self.sites = loadtxt(self.sites_file, '4a', usecols=(0,))

        self.G_file = G_file
        self.G = EpochalData(G_file)
        self.G_file_overwrite = G_file_overwrite

        if extra_info is None:
            self.extra_info = {}
        else:
            self.extra_info = extra_info

        if extra_info_attrs is None:
            self.extra_info_attrs = {}
        else:
            self.extra_info_attrs = extra_info_attrs

        
    def _check_pollitz_outputs_existence(self):
        for day in self.epochs:
            for fltno in range(0, self.num_subflts):
                fn = self._form_file_name(day, fltno)
                assert exists(fn), "File %s is not exists! Abort."%fn

    def _check_hdf5_existence(self):
        if self.G_file_overwrite:
            if exists(self.G_file):
                print('Output HDF5 %s will be overwritten.'%self.G_file)
            delete_if_exists(self.G_file)
        else:
            assert not exists(self.G_file), \
                   "Output HDF5 already exists!"

    def _form_file_name(self, day, fltno):
        fn1 = 'day_%04d_flt_%04d.out'%(day,fltno)
        fn2 = join(self.pollitz_outputs_dir, fn1)
        return fn2
    
    def _read_a_day(self, day):        
        read_file = lambda fn : loadtxt(fn, usecols=(2,3,4)).flatten()

        num_sites = len(self.sites)
        G = zeros((num_sites*3, self.num_subflts))
        for fltno in range(0, self.num_subflts):
            fn = self._form_file_name(day, fltno)
            # print("Reading file %s ..."%fn)
            col = read_file(fn)
            assert col.shape[0] == G.shape[0]
            G[:,fltno] = col
        return G

    def _write_G_to_hdf5(self):    
        for day in self.epochs:
            print("Read files at day = %04d ..."%day)
            G = self._read_a_day(day)
            if day == 0:
                self.G.set_epoch_value(0, G)
            else:
                G0 = self.G.get_epoch_value(0)
                self.G.set_epoch_value(day, G + G0)

    def _write_info_to_hdf5(self):
        sites = self.sites
        self.G.set_info('sites', [ii for ii in sites])
        self.G.set_info('num_subflts', self.num_subflts)

    def _write_extra_info_to_hdf5(self):        
        for key, value in self.extra_info.items():
            self.G.set_info(key,value)
        for key, attrs in self.extra_info_attrs.items():
            for key_attr, value_attr in attrs.items():
                self.G.set_info_attr(key, key_attr, value_attr)

    def __call__(self):
        self._check_pollitz_outputs_existence()
        self._check_hdf5_existence()
        self._write_G_to_hdf5()
        self._write_info_to_hdf5()
        self._write_extra_info_to_hdf5()

    
