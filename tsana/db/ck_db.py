import numpy as np
import sqlite3
from pylab import plt

site = '_FUK'
cmpt = 'n'
with sqlite3.connect('~observation.db') as conn:
    c = conn.cursor()
    tp = c.execute('select day, %s from tb_linres where site=? order by day'%cmpt, (site,)).fetchall()
    t = [ii[0] for ii in tp]
    y = [ii[1] for ii in tp]

plt.plot(t, y,'x')
    
##tp = np.loadtxt('../pre_fit/linres/%s.%s.lres'%(site,cmpt))
tp = np.loadtxt('../sea_floor/cumu_post/%s.original'%(site))
t = tp[:,0]
y = tp[:,2]
plt.plot(t, y,'o')

plt.show()
