import sqlite3

with sqlite3.connect('pred_disp.db') as conn:
    c = conn.cursor()
    tp = c.execute('select e from tb_cumu_disp_obs where site="J550" order by day;')
    tp = tp.fetchall()
    e_cumu = [ii[0] for ii in tp]

    tp = c.execute('select e from view_co_disp_obs where site="J550";')
    tp = tp.fetchall()
    e_co = tp[0]

    tp = c.execute('select e from view_post_disp_obs where site="J550" order by day;')
    tp = tp.fetchall()
    e_post = [ii[0] for ii in tp]


from pylab import plt
import numpy as np

plt.plot(e_cumu)
plt.plot(np.asarray(e_post) + e_co)

plt.show()
