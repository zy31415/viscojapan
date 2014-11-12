import sqlite3

import sqlite3

with sqlite3.connect('../sites_database/gps_sites.sqlite3') as conn:
    c = conn.cursor()
    tp = c.execute('select distinct network from tb_networks;').fetchall()
    print(tp)

    # stations in Korea
    tp = c.execute('''
select distinct tb_networks.id, tb_sites.lon, tb_sites.lat
from tb_networks
join tb_sites
on tb_networks.id=tb_sites.id
where tb_networks.network = ?;
''', ("KOREAN",)).fetchall()

    with open('korea.gmt','wt') as fid:
        for ii in tp:
            fid.write('%f %f %s\n'%(ii[1], ii[2], ii[0]))

    # stations in China
    tp = c.execute('''
select distinct tb_networks.id, tb_sites.lon, tb_sites.lat
from tb_networks
join tb_sites
on tb_networks.id=tb_sites.id
where tb_networks.network in ("CMONOC","TEONET");
''',).fetchall()

    with open('china.gmt','wt') as fid:
        for ii in tp:
            fid.write('%f %f %s\n'%(ii[1], ii[2], ii[0]))

    # stations in Japan
    tp = c.execute('''
select distinct tb_networks.id, tb_sites.lon, tb_sites.lat
from tb_networks
join tb_sites
on tb_networks.id=tb_sites.id
where tb_networks.network = "GEONET";
''',).fetchall()

    with open('japan.gmt','wt') as fid:
        for ii in tp:
            fid.write('%f %f %s\n'%(ii[1], ii[2], ii[0]))

        # IGS stations
    tp = c.execute('''
select distinct tb_networks.id, tb_sites.lon, tb_sites.lat
from tb_networks
join tb_sites
on tb_networks.id=tb_sites.id
where tb_networks.network = "IGSSTA";
''',).fetchall()

    with open('igs.gmt','wt') as fid:
        for ii in tp:
            fid.write('%f %f %s\n'%(ii[1], ii[2], ii[0]))
    
    

