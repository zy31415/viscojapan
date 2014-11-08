import sqlite3

import numpy as np

def create_db(db_name):
    # create talbe
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE if not exists tb_sites (
    id text primary key,
    lon real,
    lat real,
    ref text
    )''')

        c.execute('''CREATE TABLE if not exists tb_networks (
    id text,
    network text,
    ref text,
    primary key(id, network),
    FOREIGN KEY(id) REFERENCES tb_sites(id)
    )''')
        # exe this command everytime if you want foreign key constraint to work.
        c.execute('PRAGMA foreign_keys = ON;')      
    
        conn.commit()

def load_sites_position_file(sites_position_file, db_file, if_ref=True):
    if if_ref:
        sites_pos = np.loadtxt(sites_position_file,'4a, f, f, 20a')
        sites_pos = [(ii[0].decode(),float(ii[1]), float(ii[2]), ii[3].decode())
                     for ii in sites_pos]
    else:
        sites_pos = np.loadtxt(sites_position_file,'4a, f, f')
        sites_pos = [(ii[0].decode(),float(ii[1]), float(ii[2]), '')
                     for ii in sites_pos]
    

    sites_added = []
    sites_skipped = []
    
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys = ON;')
        for si in sites_pos:
            site = si[0]
            try:
                c.execute('insert into tb_sites values (?,?,?,?)', si)
                sites_added.append(site)
            except sqlite3.IntegrityError:
                sites_skipped.append(site)
                pass
                
        conn.commit()
    return sites_added, sites_skipped

def load_sites_networks_file(sites_networks_file, db_file):
    sites_network = np.loadtxt(sites_networks_file,'4a, 6a, 20a')
    sites_network = [(ii[0].decode(), ii[1].decode(), ii[2].decode()) for ii in sites_network]

    sites_added = []
    sites_skipped = []
    
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys = ON;')
        for si in sites_network:
            site = si[0]
            try:
                c.execute('insert into tb_networks values (?,?,?)', si)
                sites_added.append(site)
            except sqlite3.IntegrityError:
                sites_skipped.append(site)
                pass
        conn.commit()
    return sites_added, sites_skipped

create_db('gps_sites.db')
load_sites_position_file('Baek_2012/sites_position', 'gps_sites.db')
load_sites_networks_file('Baek_2012/sites_network', 'gps_sites.db')

load_sites_position_file('Zhao_2012/sites_pos', 'gps_sites.db')
load_sites_networks_file('Zhao_2012/sites_networks', 'gps_sites.db')

load_sites_position_file('Wang_2011/sites_pos', 'gps_sites.db')
load_sites_networks_file('Wang_2011/sites_networks', 'gps_sites.db')

load_sites_position_file('NGL/sites', 'gps_sites.db')
