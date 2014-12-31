from os.path import join
try:
    import sqlite3
except ImportError:
    print("    Cannot import sqlite3.")

from point_in_polygon import Polygon

import numpy as np

from ..utils import get_this_script_dir

this_script_dir = get_this_script_dir(__file__)

file_database = join(this_script_dir, 'gps_sites.sqlite3')

__all__ = ['get_pos_dic', 'get_pos', 'get_networks_dic','get_pos_dic_of_a_network',
           'gen_network_sites_file','get_true_name_by_id',
           'choose_sites_in_polygon']

def get_pos_dic():
    with sqlite3.connect(file_database) as conn:
        c = conn.cursor()
        tp = c.execute('select id,lon,lat from tb_sites;').fetchall()

    return {ii[0]:(ii[1], ii[2]) for ii in tp}

def get_pos(sites):
    lons=[]
    lats=[]
    pos=get_pos_dic()
    for site in sites:
        tp=pos[site]
        lons.append(tp[0])
        lats.append(tp[1])
    return np.asarray(lons, 'float'), np.asarray(lats, 'float')

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
    

def get_true_name_by_id(id):
    with sqlite3.connect(file_database) as conn:
        c = conn.cursor()
        name = c.execute('select name from tb_sites where id=?;', (id,)).fetchall()
    if name[0][0] is None:
        return id
    return name[0][0]

def get_pos_dic_of_a_network(network):
    with sqlite3.connect(file_database) as conn:
        c = conn.cursor()
        tp = c.execute('''
select tb_sites.id, lon, lat from tb_sites
join tb_networks on tb_sites.id = tb_networks.id
where network = ?
''', (network,)).fetchall()

    return {ii[0]:(ii[1], ii[2]) for ii in tp}

def gen_network_sites_file(network, sites_file, header=None):
    sites_dic = get_pos_dic_of_a_network(network)
    _tp = []
    for site in sorted(sites_dic):
        lon, lat = sites_dic[site]
        _tp.append((site, lon, lat))

    _arr = np.array(_tp, 'U4, f, f')
    if header is None:
        header='''Sites list of network: "%s"

id lon lat'''%network
    np.savetxt(sites_file, _arr, fmt='%s %f %f', header=header)
    

def get_maxmin_lonlat():
    tp = np.loadtxt(sites_file,'4a,2f')
    lons = [ii[1][0] for ii in tp]
    lats = [ii[1][1] for ii in tp]

    return np.amin(lons),np.amax(lons), np.amin(lats),np.amax(lats)
    
def remove_sites_from(sites0, sites1):
    out = []
    for site in sites0:
        if site not in sites1:
            out.append(site)
    return out


def choose_sites_in_polygon(sites,x,y):
    lons, lats = get_pos(sites)    
    p = Polygon(x,y)
    ch = []
    for lon, lat in zip(lons, lats):
        mindst = p.is_inside(lon, lat)
        if mindst < 0:
            ch.append(False)
        else:
            ch.append(True)
    return np.asarray(ch)
