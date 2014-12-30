import sqlite3

class PercentageOfMechanisms(object):
    def __init__(self,
                 file_pred_db,
                 sites,
                 ):
        self.file_pred_db = file_pred_db
        self.sites = sites

    def percentage_Rco(self):
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            c.execute('select e, n, u from view_post_disp_pred order by epoch, sites;')
        

    def percentage_Raslip(self):
        pass

    def percentage_Easlip(self):
        pass
        
