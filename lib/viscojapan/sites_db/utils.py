from os.path import join
import sqlite3

from ..utils import get_this_script_dir

this_script_dir = get_this_script_dir(__file__)

file_database = join(this_script_dir, 'gps_sites.sqlite3')

__all__ = ['get_pos_dic', 'get_networks_dic','get_pos_dic_of_a_network']

def get_pos_dic():
    with sqlite3.connect(file_database) as conn:
        c = conn.cursor()
        tp = c.execute('select * from tb_sites;').fetchall()

    return {ii[0]:(ii[1], ii[2]) for ii in tp}

def get_networks_dic():
    with sqlite3.connect(file_database) as conn:
        c = conn.cursor()
        networks = c.execute('select distinct network from tb_networks;').fetchall()
        out = {}
        for network in networks:
            sites = c.execute('select id from tb_networks where network=?;',
                              network).fetchall()
            out[network[0]]=sites
        return out
            

    return {ii[0]:(ii[1], ii[2]) for ii in tp}
    

def get_pos_dic_of_a_network(network):
    with sqlite3.connect(file_database) as conn:
        c = conn.cursor()
        tp = c.execute('''
select tb_sites.id, lon, lat from tb_sites
join tb_networks on tb_sites.id = tb_networks.id
where network = ?
''', (network,)).fetchall()

    return {ii[0]:(ii[1], ii[2]) for ii in tp}
    
