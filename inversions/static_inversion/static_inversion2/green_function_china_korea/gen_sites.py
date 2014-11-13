import numpy as np

import viscojapan as vj

pos_dic = vj.sites_db.get_pos_dic()

_txt = np.array([(key, pos_dic[key][0], pos_dic[key][1])for key in sorted(pos_dic)],
                dtype=('U4,f,f'))

np.savetxt('sites_china_korea', _txt, fmt='%s %f %f')
    
