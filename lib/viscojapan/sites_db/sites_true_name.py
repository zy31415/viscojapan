import sqlite3

__author__ = 'zy'

from .share import file_gps_sites_db

def get_site_true_name(site):
    try:
        sites = site
        return [get_site_true_name(site) for site in sites]
    except TypeError:
        with sqlite3.connect(file_gps_sites_db) as conn:
            c = conn.cursor()
            name = c.execute('select name from tb_sites where id=?;', (site.id,)).fetchall()
        assert len(name)==1
        name = name[0][0]
        if name is None:
            name  = site.id
        return name
