import sqlite3

from ..sites import Sites, Site

from .share import file_gps_sites_db


__author__ = 'zy'
__all__ = ['get_sites_from_network']

def get_sites_from_network(network):
    with sqlite3.connect(file_gps_sites_db) as conn:
        c = conn.cursor()
        tp = c.execute('''
select tb_sites.id, lon, lat from tb_sites
join tb_networks on tb_sites.id=tb_networks.id
where network = ?
order by tb_sites.id
''', (network,)).fetchall()
    return Sites([Site(id=ii[0], lon=ii[1], lat=ii[2]) for ii in tp])
