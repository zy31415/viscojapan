import sqlite3

from pylab import plt

db_file = '~pred_disp.db'

site = 'J799'



def read_ts_from_table(table, site, cmpt):
    with sqlite3.connect(db_file) as conn:
        c = conn.cursor()
        res = c.execute('select day,{cmpt} from {table} where site=? order by day'\
                        .format(cmpt=cmpt, table=table),
                        (site,)).fetchall()
        epochs = [ii[0] for ii in res]
        ys = [ii[1] for ii in res]
    return epochs, ys

epochs, ys = read_ts_from_table(
    'view_total_disp_added',
    site,
    'e'
    )
plt.plot(epochs, ys)

epochs, ys = read_ts_from_table(
    'tb_cumu_disp_pred',
    site,
    'e'
    )
plt.plot(epochs, ys)

plt.show()
    
