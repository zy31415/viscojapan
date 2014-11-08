import sqlite3

__doc__ = 'Select GEONET stations and add into the database'

def get_sites_pos_dic():
    with sqlite3.connect('gps_sites.db') as conn:
        c = conn.cursor()
        c.execute('PRAGMA foreign_keys = ON;')
        sites_pos = c.execute('select * from tb_sites;').fetchall()
    return {ii[0]:(ii[1],ii[2]) for ii in sites_pos}
    
def check_if_in_region(lon, lat, west, south, east, north):
    if (lon>west) and (lon<east) and (lat>south) and (lat<north):
        return True
    return False

def check_in_GEONET(lon, lat):
    nankaido = (138.52, 41.25, 147.89, 45.78)
    honshu = (132.57, 32.19, 142.76, 41.55)
    kyushu = (128.34, 29.35, 132.54, 34.77)
    ryukyu_trench = (122.20, 23.31, 130.92, 28.18)
    if check_if_in_region(lon, lat, *nankaido):
        return True
    if check_if_in_region(lon, lat, *honshu):
        return True
    if check_if_in_region(lon, lat, *kyushu):
        return True
    if check_if_in_region(lon, lat, *ryukyu_trench):
        return True
    return False

sites_GEONET = []
    
sites_pos = get_sites_pos_dic()
for site, pos in sites_pos.items():
    if check_in_GEONET(*pos):
        sites_GEONET.append(site)

with sqlite3.connect('gps_sites.db') as conn:
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON;')
    for site in sites_GEONET:
        try:
            c.execute('insert into tb_networks values (?, "GEONET", "");',
                      (site,))
        except sqlite3.IntegrityError:
            print('%s is already in GEONET.'%site)
            pass
    conn.commit()

