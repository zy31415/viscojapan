import sqlite3

__all__ = ['PredDispToDatabaseWriter']

class PredDispToDatabaseWriter(object):
    def __init__(self,
                 pred_disp,
                 db_file = 'pred_disp.db',                 
                 ):
        self.pred_disp = pred_disp

        self.epochs = self.pred_disp.epochs
        self.num_epochs = len(self.epochs)

        self.filter_sites = self.pred_disp.filter_sites
        
        self.db_file = db_file

    def create_database(self):
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()

            # Create table        
            c.execute('''CREATE TABLE IF NOT EXISTS tb_E_cumu_slip
                         (site text,
                         day int,
                         e real,
                         n real,
                         u real,
                         PRIMARY KEY (site, day)
                         )
                         ''')

            c.execute('''CREATE TABLE IF NOT EXISTS tb_R_co
                         (site text,
                         day int,
                         e real,
                         n real,
                         u real,
                         PRIMARY KEY (site, day)
                         )
                         ''')

            c.execute('''CREATE TABLE IF NOT EXISTS tb_R_aslip
                         (site text,
                         day int,
                         e real,
                         n real,
                         u real,
                         PRIMARY KEY (site, day)
                         )
                         ''')

            c.execute('''CREATE VIEW IF NOT EXISTS view_E_co
                         AS 
                         SELECT site,e,n,u FROM tb_E_cumu_slip where day=0                         
                         ''')

            c.execute('''CREATE VIEW IF NOT EXISTS view_E_aslip
                         AS 
                         SELECT tb_E_cumu_slip.site as site,
                                tb_E_cumu_slip.e - view_E_co.e as e,
                                tb_E_cumu_slip.n - view_E_co.n as n,
                                tb_E_cumu_slip.u - view_E_co.u as u
                         FROM view_E_co
                         JOIN tb_E_cumu_slip
                         ON view_E_co.site = tb_E_cumu_slip.site;
                         ''')

            c.execute('''CREATE VIEW IF NOT EXISTS view_R_cumu_slip
                         AS 
                         SELECT tb_R_co.site as site,
                                tb_R_co.day as day,
                                tb_R_co.e + tb_R_aslip.e as e,
                                tb_R_co.n + tb_R_aslip.n as n,
                                tb_R_co.u + tb_R_aslip.u as u
                         FROM tb_R_co
                         JOIN tb_R_aslip
                         ON tb_R_co.site = tb_R_aslip.site
                         AND tb_R_co.day = tb_R_aslip.day;
                         ''') 

            c.execute('''CREATE VIEW IF NOT EXISTS view_total_disp_added
                         AS 
                         SELECT tb_E_cumu_slip.site as site,
                                tb_E_cumu_slip.day as day,
                                tb_E_cumu_slip.e + view_R_cumu_slip.e as e,
                                tb_E_cumu_slip.n + view_R_cumu_slip.n as n,
                                tb_E_cumu_slip.u + view_R_cumu_slip.u as u
                         FROM tb_E_cumu_slip
                         JOIN view_R_cumu_slip
                         ON tb_E_cumu_slip.site = view_R_cumu_slip.site
                         AND tb_E_cumu_slip.day = view_R_cumu_slip.day;
                         ''')

            c.execute('''CREATE TABLE IF NOT EXISTS tb_total_disp_pred
                         (site text,
                         day int,
                         e real,
                         n real,
                         u real,
                         PRIMARY KEY (site, day)
                         )
                         ''')

            c.execute('''CREATE TABLE IF NOT EXISTS tb_cumu_disp_obs
                         (site text,
                         day int,
                         e real,
                         n real,
                         u real,
                         PRIMARY KEY (site, day)
                         )
                         ''')

            c.execute('''CREATE VIEW IF NOT EXISTS view_co_disp_obs
                         AS 
                         SELECT site, e, n, u
                         FROM tb_cumu_disp_obs
                         WHERE day = 0;
                         ''')
            
            c.execute('''CREATE VIEW IF NOT EXISTS view_post_disp_obs
                         AS
                         SELECT tb_cumu_disp_obs.site as site,
                                tb_cumu_disp_obs.day as day,
                                tb_cumu_disp_obs.e - view_co_disp_obs.e as e,
                                tb_cumu_disp_obs.n - view_co_disp_obs.n as n,
                                tb_cumu_disp_obs.u - view_co_disp_obs.u as u
                         FROM tb_cumu_disp_obs
                         JOIN view_co_disp_obs
                         ON tb_cumu_disp_obs.site = view_co_disp_obs.site;
                         ''')

            # Save (commit) the changes
            conn.commit()

    def _insert_into_database(self, table_name, items, duplication='REPLACE'):        
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            c.executemany('INSERT OR {duplication} INTO {table} VALUES (?,?,?,?,?);'\
                          .format(duplication=duplication, table=table_name),
                          items)
            conn.commit()

    def insert_total_disp_from_result(self, duplication='REPLACE'):
        items = []
        for nth, epoch in enumerate(self.epochs):
            disps = self.pred_disp.result_file_reader.get_disp_at_epoch(epoch)
            disps = disps.reshape([-1,3])
            sites = self.pred_disp.result_file_reader.sites
            items += [(site, int(epoch), slip[0], slip[1], slip[2])
                     for site, slip in zip(self.filter_sites, disps)]
        self._insert_into_database('tb_total_disp_pred', items, duplication)
        

    def insert_E_cumu_slip(self, duplication='REPLACE'):
        items = []
        for nth, epoch in enumerate(self.epochs):
            disps = self.pred_disp.E_cumu_slip(nth).reshape([-1,3])
            items += [(site, int(epoch), slip[0], slip[1], slip[2])
                     for site, slip in zip(self.filter_sites, disps)]
        self._insert_into_database('tb_E_cumu_slip', items, duplication)

    def insert_R_co(self, duplication='REPLACE'):
        items = []
        for epoch in self.epochs:
            disps = self.pred_disp.R_co(epoch).reshape([-1,3])
            items += [(site, int(epoch), slip[0], slip[1], slip[2])
                     for site, slip in zip(self.filter_sites, disps)]
        self._insert_into_database('tb_R_co', items, duplication)

    def insert_R_aslip(self, duplication='REPLACE'):
        items = []
        for epoch in self.epochs:
            disps = self.pred_disp.R_aslip(epoch).reshape([-1,3])
            items += [(site, int(epoch), slip[0], slip[1], slip[2])
                     for site, slip in zip(self.filter_sites, disps)]
        self._insert_into_database('tb_R_aslip', items, duplication)
        

    def insert_all(self, duplication='REPLACE'):
        self.insert_total_disp_from_result(duplication)
        self.insert_E_cumu_slip(duplication)
        self.insert_R_co(duplication)
        self.insert_R_aslip(duplication)
