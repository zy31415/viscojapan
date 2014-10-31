import h5py

from pylab import plt

import viscojapan as vj

nreses =[]
rakes = []

com  = vj.ComputeMoment('../../fault_model/fault_bott60km.h5',
                        'earth.model_He63km_VisM1.0E19'
                        )

mos = []
mws = []
for ano in range(30):
    with h5py.File('outs/ano_%02d.h5'%ano,'r') as fid:
        Bm = fid['Bm'][...]
        slip = Bm[0:-1,:]
        mo, mw = com.moment(slip)
        mos.append(mo)
        mws.append(mw)
        
##
##        rake = fid['nlin_pars/rake'][...]
##        rakes.append(rake)
##    
##plt.semilogx(nreses, rakes,'o')
##plt.ylabel('rake')
##plt.xlabel('weighted residual norm')
##plt.xlim([0.7, 4])
##plt.savefig('plots/rake_residual.png')
##plt.show()
