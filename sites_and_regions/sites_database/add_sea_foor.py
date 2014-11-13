import sqlite3

import numpy as np

tp = np.loadtxt('sites_seafloor','4a,f,f',usecols=(1,2,3))

cmd1 = [(float(ii[1]),float(ii[2]),ii[0].decode()) for ii in tp]

cmd2 = [(ii[0].decode(),'SEAFLOOR','Sato_2011') for ii in tp]

cmd3 = [(ii[0].decode(), float(ii[1]),float(ii[2]),'') for ii in tp]

with sqlite3.connect('gps_sites.sqlite3') as conn:
    c = conn.cursor()
    c.executemany('insert into tb_sites values (?,?,?,?);', cmd3)
    #c.executemany('update tb_sites set lon = ?, lat = ? where id = ?;', cmd1)
    
    #c.executemany('insert into tb_networks values (?,?,?);', cmd2)
    conn.commit()

