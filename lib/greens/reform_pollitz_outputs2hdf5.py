from os.path import join, exists

from numpy import NaN, loadtxt, asarray
import h5py

class ReformPollitzOutputs2HDF5(object):
    ''' This class reform the original outputs by STATIC1D & VISCO1D
into a HDF5 file.
'''
    def __init__(self):
        # initialize the following variables!
        self.days_of_epochs = []
        self.no_of_subfaults = NaN
        self.pollitz_outputs_dir = ""
        
        self.file_stations_in = ""
        
        self.output_filename_hdf5 = ""

        self.He = NaN
        self.visM = NaN
        self.visK = NaN
        self.lmax = NaN


    def _assert_initialization(self):
        assert len(self.days_of_epochs) != 0, "Have you initialize the object?"
        assert self.no_of_subfaults != NaN, "Have you initialize the object?"
        assert self.pollitz_outputs_dir != "", "Have you initialize the object?"
        assert self.output_filename_hdf5 != "", "Have you initialize the object?"
        assert self.He != NaN
        assert self.visM != NaN
        assert self.visK != NaN
        assert self.lmax != NaN
        assert self.file_stations_in != ""
        
    def _check_pollitz_outputs_existence(self):
        for day in self.days_of_epochs:
            for fltno in range(0, self.no_of_subfaults):
                fn = self._form_file_name(day, fltno)
                assert exists(fn), "File %s is not exists! Abort."%fn

    def _check_hdf5_existence(self):
        assert not exists(self.output_filename_hdf5), \
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
        with h5py.File(self.output_filename_hdf5, 'w-') as fid:
            for day in self.days_of_epochs:
                print(day)
                G = self._read_a_day(day)
                if day == 0:
                    fid['0000'] = G                   
                else:
                    fid['%04d'%day] = (G + fid['0000'])

    def _get_sites(self):
        tp = loadtxt(self.file_stations_in,'2f,4a')
        sites = [ii[1] for ii in tp]
        return sites
    
    def _get_site_cmpt(self):
        site_cmpt = []
        for site in self._get_sites():
            site_cmpt.append(site+b'-e')
            site_cmpt.append(site+b'-n')
            site_cmpt.append(site+b'-u')
        return site_cmpt

    def _write_info_to_hdf5(self):            
        with h5py.File(self.output_filename_hdf5, 'a') as fid:
            fid['info/sites'] = self._get_sites()
            
            fid['info/rows'] = self._get_site_cmpt()

            fid['info/He'] = self.He
            fid['info/He'].attrs['unit'] = 'km'

            fid['info/visM'] = self.visM
            fid['info/visM'].attrs['unit'] = 'Pa.s'

            fid['info/visK'] = self.visK
            fid['info/visK'].attrs['unit'] = 'Pa.s'
            
            fid['info/lmax'] = self.lmax

            fid['info/days_of_epochs'] = self.days_of_epochs

            fid['info/no_of_subfaults'] = self.no_of_subfaults

    def __call__(self):
        self._assert_initialization()
        self._check_pollitz_outputs_existence()
        self._check_hdf5_existence()
        self._write_G_to_hdf5()
        self._write_info_to_hdf5()

    
            
        

    



     
        
        
