from os.path import exists

import h5py
from numpy import loadtxt, asarray

class GFilter(object):
    ''' Fliter a G matrix according a new station list.
'''
    def __init__(self):
        self.G_old = ''
        self.G_new = ''
        self.sites_file = ''

    def _verify_initialization(self):
        assert exists(self.G_old), "Old HDF doesn't exist."
        assert not exists(self.G_new), "New HDF exists."
        assert exists(self.sites_file), "sites file doesn't exist."
        
    def _days_of_epochs(self):
        with h5py.File(self.G_old) as fid:
            days = fid['/info/days_of_epochs'][...]
        return days

    def _new_sites(self):
        sites = loadtxt(self.sites_file,'4a')
        return sites

    def _new_rows(self):
        rows = []
        for site in self._new_sites():
            rows.append(site + b'-e')
            rows.append(site + b'-n')
            rows.append(site + b'-u')
        return rows

    def _old_rows(self):
        with h5py.File(self.G_old) as fid:
            rows = fid['/info/rows'][...]
        return rows

    def _gen_ch_rows(self):
        rows_old = list(self._old_rows())
        ch_rows=[]
        for row in self._new_rows():
            ch_rows.append(rows_old.index(row))
        ch_rows=asarray(ch_rows)
        return ch_rows
    
    def __call__(self):
        self._verify_initialization()
        
        ch_rows = self._gen_ch_rows()
        days_of_epochs = self._days_of_epochs()
        
        with h5py.File(self.G_new, 'w-') as hdf_new:            
            hdf_old = h5py.File(self.G_old,'r')
            for day in days_of_epochs:
                G_old = hdf_old['%04d'%day][...]                
                G_new = G_old[ch_rows,:]
                hdf_new['%04d'%day] = G_new
                
            hdf_old.copy('info', hdf_new)

            del hdf_new['/info/sites']
            hdf_new['/info/sites'] = self._new_sites()
            
            del hdf_new['/info/rows']
            hdf_new['/info/rows'] = self._new_rows()

            hdf_old.close()
            
        
        
