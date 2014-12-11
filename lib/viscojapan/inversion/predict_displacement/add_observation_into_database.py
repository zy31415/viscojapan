import sqlite3

from ...epochal_data import EpochalFileReader

__all__ = ['ObsToDatabaseWriter']

class ObsToDatabaseWriter(object):
    def __init__(self,
                 file_cumu_disp_obs,
                 db_file = '~pred_disp.db',                 
                 ):
        self.file_cumu_disp_obs = file_cumu_disp_obs

        self.db_file = db_file

    def create_database(self):
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()

            c.execute('''CREATE TABLE IF NOT EXISTS tb_cumu_disp_obs
                         (site text,
                         day int,
                         e real,
                         n real,
                         u real,
                         PRIMARY KEY (site, day)
                         );
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
##
            # Save (commit) the changes
            conn.commit()

    def _insert_into_database(self, table_name, items, duplication='REPLACE'):        
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            c.executemany('INSERT OR {duplication} INTO {table} VALUES (?,?,?,?,?);'\
                          .format(duplication=duplication, table=table_name),
                          items)
            conn.commit()

    def insert_cumu_disp_obs(self, duplication='REPLACE'):
        reader = EpochalFileReader(self.file_cumu_disp_obs)
        epochs = reader.get_epochs()
        sites = reader['sites']
        sites = [site.decode() for site in sites]
        
        items = []
        for nth, epoch in enumerate(epochs):
            disps = reader[epoch].reshape([-1,3])
            items += [(site, int(epoch), disp[0], disp[1], disp[2])
                     for site, disp in zip(sites, disps)]
        self._insert_into_database('tb_cumu_disp_obs', items, duplication)        
 
