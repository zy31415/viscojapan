import shutil
from os.path import join, exists

import numpy as np

import viscojapan as vj

__all__=['copy_and_revise_sd_file','GenSD','GenUniformSD','GenOzawaSD']

def copy_and_revise_sd_file(file_sd_original, file_seafloor_sd, file_sd_out, sd = None):
    assert not exists(file_sd_out)
    assert exists(file_sd_original)
    assert exists(file_seafloor_sd)
    shutil.copyfile(file_sd_original, file_sd_out)
    ep = vj.EpochalDisplacementSD(file_sd_out)
    seafloor = np.loadtxt(file_seafloor_sd, '4a,i, 3f')

    for ii in seafloor:
        site = ii[0].decode()
        day = ii[1]
        if sd is None:
            sd = ii[2]
        assert len(sd) == 3
        print(site, day, sd)

        ep.set_value_at_site(site, 'e', day, sd[0])
        ep.set_value_at_site(site, 'n', day, sd[1])
        ep.set_value_at_site(site, 'u', day, sd[2])

class GenSD(object):
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

class GenUniformSD(object):
    def __init__(self,
                 sites,
                 days,
                 sd_seafloor,
                 sd_inland,
                 sd_co,
                 ):
        self.sites = sites
        self.ch_inland = vj.choose_inland_GPS(self.sites)
        self.num_obs = 3*len(self.sites)
        
        self.days = days
        self.sd_seafloor = sd_seafloor
        self.sd_inland = sd_inland
        self.sd_co = sd_co
    
    def _gen_sd(self, epoch):
        if epoch==0:
            data = np.ones([self.num_obs,1],float) * self.sd_co
        else:
            data = np.ones([self.num_obs,1],float) * self.sd_inland
        data = data.reshape([-1,3])
        data[~self.ch_inland,:] = self.sd_seafloor
        return data.reshape([-1,1])

    def save(self, fn):
        num_obs = 3*len(self.sites)
        for day in self.days:
            ep = vj.EpochalData(fn)
            ep[int(day)] = self._gen_sd(day)
        ep['sites'] = self.sites
        ep['max inland sd'] = self.sd_inland
        ep['min inland sd'] = self.sd_inland
        ep['mean inland sd'] = self.sd_inland
        ep['median inland sd'] = self.sd_inland
        ep['seafloor sd'] = self.sd_seafloor
        
class GenOzawaSD(object):
    def __init__(self,
                 sites,
                 days,
                 sd_seafloor
                 ):
        self.sites = sites
        self.ch_inland = vj.choose_inland_GPS(self.sites)
        self.num_obs = 3*len(self.sites)
        self.ch_inland = vj.choose_inland_GPS_for_cmpts(self.sites)
        
        self.days = days
        self.sd_seafloor = sd_seafloor
        
    def _gen_sd(self):
        data = np.ones([self.num_obs,1],float)
        data[2::3] = 5.
        data[~self.ch_inland] = self.sd_seafloor
        return data.reshape([-1,1])

    def save(self, fn):
        num_obs = 3*len(self.sites)
        for day in self.days:
            ep = vj.EpochalData(fn)
            ep[int(day)] = self._gen_sd()
        ep['sites'] = self.sites
        ep['max sd'] = 5.
        ep['min sd'] = 1.
        ep['mean sd'] = np.mean(self._gen_sd())
        ep['median sd'] = np.median(self._gen_sd())
        
        
    
