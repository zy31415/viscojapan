import shutil
from os.path import join, exists

import h5py
import numpy as np

import viscojapan as vj

__all__=['copy_and_revise_sd_file','GenSD',
         'GenUniformOnshoreSDWithInfiniteSeafloorSD']

__doc__ = ''' This script contains functions and classes used to
generate SD file for the inversion.
A final SD file is generated in two steps:
Step 1: Generate a SD file assumimg seafloor SD is infinite.
Step 2: Modify seafloor SD value in the generated SD file in step 1
        according to file_seafloor_sd.
'''

def copy_and_revise_sd_file(file_sd_original, file_seafloor_sd, file_sd_out, sd = None):
    assert not exists(file_sd_out)
    assert exists(file_sd_original)
    assert exists(file_seafloor_sd)

    shutil.copyfile(file_sd_original, file_sd_out)
    ep = vj.EpochalDisplacementSD(file_sd_out)
    seafloor = np.loadtxt(file_seafloor_sd, '4a,i, 3f')

    epochs = ep.get_epochs()
    
    for ii in seafloor:
        site = ii[0].decode()
        day = ii[1]

        assert day in epochs, "Original sd file doesn't have data on day %d !"%day        
        
        if sd is None:
            sd = ii[2]
        assert len(sd) == 3
        print(site, day, sd)

        ep.set_value_at_site(site, 'e', day, sd[0])
        ep.set_value_at_site(site, 'n', day, sd[1])
        ep.set_value_at_site(site, 'u', day, sd[2])
        ep['seafloor sd/%s_day_%04d'%(site, day)] = sd

class GenSD(object): #TODO: This class is dated.
    def __init__(self,
                 dir_linres,
                 sites,
                 days
                 ):
        self.dir_linres = dir_linres
        self.sites = sites
        self.num_sites = len(self.sites)
        self.days = days

    def _read_file_linres(self, site, cmpt):
        tp = np.loadtxt(
            join(self.dir_linres, '%s.%s.lres'%(site.decode(), cmpt)))
        t = tp[:,0]
        assert np.all(np.diff(t)) > 0
        sd = tp[:,3]
        return t, sd

    def _interp_standard_deviation(self, site, cmpt):        
        t_eq = 55631
        t, sd = self._read_file_linres(site, cmpt)       
        sd_interp = np.interp(self.days + t_eq, t, sd)
        return sd_interp

    def _gen_data_matrix(self):
        print('Generating data matrix ...')
        data = np.zeros([self.num_sites*3, len(self.days)])
        for nth, site in enumerate(self.sites):
            print(nth, site)
            for mth, cmpt in enumerate(['e', 'n', 'u']):
                sd = self._interp_standard_deviation(site, cmpt)
                data[nth*3+mth, :] = sd
        self.data = data

    def save(self, fn):
        self._gen_data_matrix()
        for day in self.days:
            ep = vj.EpochalData(fn)
            ep[int(day)] = self.data[:,(day,)]
        ep['sites'] = self.sites
        ep['max sd'] = np.amax(self.data)
        ep['min sd'] = np.amin(self.data)
        ep['mean sd'] = np.mean(self.data)
        ep['median sd'] = np.median(self.data)

        
class GenUniformOnshoreSDWithInfiniteSeafloorSD(object):
    def __init__(self,
                 sites,
                 days,
                 sd_co_hor,
                 sd_co_ver,
                 sd_post_hor,
                 sd_post_ver,                 
                 sd_seafloor = 1e99
                 ):
        self.sites = sites
        self.ch_inland = self._choose_inland_GPS()
        self.num_sites = len(self.sites)
        self.num_obs = 3 * self.num_sites
        
        self.days = days
        self.num_epochs = len(self.days)

        self.sd_co_hor = sd_co_hor
        self.sd_co_ver = sd_co_ver
        
        self.sd_post_hor = sd_post_hor
        self.sd_post_ver = sd_post_ver
        
        self.sd_seafloor = sd_seafloor

    def _choose_inland_GPS(self):
        ch = []
        for site in self.sites:
            if site[0]=='_':
               ch.append(False)
            else:
                ch.append(True)
        return np.asarray(ch)

        

    def _gen_sd_array(self, sd_east, sd_north, sd_up):
        arr1 = np.ones(self.num_sites) * sd_east
        arr2 = np.ones(self.num_sites) * sd_north
        arr3 = np.ones(self.num_sites) * sd_up
        arr = np.vstack((arr1, arr2, arr3)).T
        arr[~self.ch_inland,:] = self.sd_seafloor
        return arr.reshape([-1,1])
        

    def _gen_sd_for_coseismic_disp(self):
        return self._gen_sd_array(self.sd_co_hor,
                                  self.sd_co_hor,
                                  self.sd_co_ver)

    def _gen_sd_for_postseismic_disp(self):
        return self._gen_sd_array(self.sd_post_hor,
                                  self.sd_post_hor,
                                  self.sd_post_ver)

    def save(self, fn):
        with h5py.File(fn,'w') as fid:
            fid.create_dataset('data3d',
                               shape=(self.num_epochs,self.num_sites,3)
                               )

            for nth, day in enumerate(self.days):
                if day == 0:
                    data = self._gen_sd_for_coseismic_disp()
                else:
                    data = self._gen_sd_for_postseismic_disp()
                fid['data3d'][nth,:,:] = data.reshape([-1,3])
            fid['sites'] = [site.encode() for site in self.sites]
            fid['sd_co_hor'] = self.sd_co_hor
            fid['sd_co_ver'] = self.sd_co_ver
            fid['sd_post_hor'] = self.sd_post_hor
            fid['sd_post_ver'] = self.sd_post_ver
            fid['sd_seafloor'] = self.sd_seafloor
