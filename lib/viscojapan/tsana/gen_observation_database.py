import glob
import sqlite3
from os.path import join, basename

import numpy as np


__all__ = ['ObservationDatatbaseWriter']

dir_tsana = '/home/zy/workspace/viscojapan/tsana/'

class ObservationDatatbaseWriter(object):
    def __init__(self,
                 dir_linres = join(dir_tsana, 'pre_fit/linres'),
                 dir_cumu_post_displacement = join(dir_tsana, 'post_fit/cumu_post_displacement/'),
                 dir_seafloor_postseismic_time_series = join(dir_tsana, 'sea_floor/cumu_post/'),
                 db_file = '~observation.db',
                 ):
        self.dir_linres = dir_linres
        self.dir_cumu_post_displacement = dir_cumu_post_displacement
        self.dir_seafloor_postseismic_time_series = dir_seafloor_postseismic_time_series
        self.db_file = db_file

    def create_database(self):
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()

            # Create table        
            c.execute('''CREATE TABLE IF NOT EXISTS tb_linres
                         (site text,
                         day int,
                         e real,
                         n real,
                         u real,
                         PRIMARY KEY (site, day)
                         )
                         ''')

            c.execute('''CREATE TABLE IF NOT EXISTS tb_cumu_post_displacement
                         (site text,
                         day int,
                         e real,
                         n real,
                         u real,
                         PRIMARY KEY (site, day)
                         )
                         ''')
    def _insert_into_database(self, table_name, items, duplication='REPLACE'):        
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            c.executemany('INSERT OR {duplication} INTO {table} VALUES (?,?,?,?,?);'\
                          .format(duplication=duplication, table=table_name),
                          items)
            conn.commit()

    def insert_linres(self, duplication='REPLACE'):
        files = glob.glob(join(self.dir_linres,'????.?.lres'))
        print('Insert linres, # of files: %d'%len(files))
        sites = [basename(ii).split('.')[-3] for ii in files]
        items = []
        for site in sites:
            tp = np.loadtxt(join(self.dir_linres,'%s.e.lres'%site))
            t = tp[:,0]
            ch = (t >= 55631)
            ts = (t[ch] - 55631)            
            es = tp[:,2][ch]

            tp = np.loadtxt(join(self.dir_linres,'%s.n.lres'%site))
            ns = tp[:,2][ch]

            tp = np.loadtxt(join(self.dir_linres,'%s.u.lres'%site))
            us = tp[:,2][ch]
            
            items += [(site, ti, ei, ni, ui) for ti, ei, ni, ui in zip(ts, es, ns, us)]

        self._insert_into_database('tb_linres', items, duplication)

    def insert_cumu_post_displacement(self, duplication='REPLACE'):
        files = glob.glob(join(self.dir_cumu_post_displacement,'????.cumu'))
        print('Insert cumu_post_disp, # of files: %d'%len(files))
        items = []
        for file in files:
            site = basename(file).split('.')[-2]
            tp = np.loadtxt(file)
            t = tp[:,0]
            es = tp[:,1]
            ns = tp[:,2]
            us = tp[:,3]

            items += [(site, ti, ei, ni, ui) for ti, ei, ni, ui in zip(t, es, ns, us)]

        self._insert_into_database('tb_cumu_post_displacement', items, duplication)

    def insert_seafloor_original(self, duplication='REPLACE'):
        files = glob.glob(join(self.dir_seafloor_postseismic_time_series, '????.original'))
        print('Insert original seafloor, # of files: %d'%len(files))

        items = []
        for file in files:
            site = basename(file).split('.')[-2]
            tp = np.loadtxt(file)
            t = tp[:,0]
            es = tp[:,1]
            ns = tp[:,2]
            us = tp[:,3]

            items += [(site, ti, ei, ni, ui) for ti, ei, ni, ui in zip(t, es, ns, us)]

        self._insert_into_database('tb_linres', items, duplication)
