import sqlite3

from .share import file_gps_sites_db
from ..sites import Site

__all__ = ['SitesDB']

class SitesDB(object):
    file_database = file_gps_sites_db

    def __init__(self):
        pass

    def get(self, id):
        with sqlite3.connect(self.file_database) as conn:
            c = conn.cursor()
            tp = c.execute('select name,lon,lat from tb_sites where id=?;',
                           (id,)).fetchall()
        assert len(tp)==1
        tp = tp[0]
        name = tp[0]
        lon = tp[1]
        lat = tp[2]
        return Site(id=id, name=name, lon=lon, lat=lat)
        

    def gets(self, ids):
        return [self.get(id) for id in ids]

