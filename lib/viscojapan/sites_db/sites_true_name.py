import sqlite3

__author__ = 'zy'
__all__ = ['get_site_true_name', 'get_sites_true_name']

from .share import file_gps_sites_db

def get_site_true_name(site_id=None, site=None):
    if site is not None:
        site_id = site.id

    with sqlite3.connect(file_gps_sites_db) as conn:
        c = conn.cursor()
        name = c.execute('select name from tb_sites where id=?;', (site_id,)).fetchall()
    assert len(name)==1
    name = name[0][0]
    if name is None:
        name  = site.id
    return name

def get_sites_true_name(sites_ids=None, sites=None):
    if sites is not None:
        sites_ids = sites.ids
    return [get_site_true_name(site_id = si) for si in sites_ids]