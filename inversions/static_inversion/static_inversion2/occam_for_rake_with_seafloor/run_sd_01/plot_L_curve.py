import h5py

from viscojapan.plots import plot_L, plt
import viscojapan as vj

nreses =[]
nroughs = []

com  = vj.MomentCalculator('../../fault_model/fault_bott60km.h5',
                        'earth.model_He63km_VisM1.0E19'
                        )
mos = []
mws = []
rakes = []
for ano in range(30):
    with h5py.File('outs/ano_%02d.h5'%ano,'r') as fid:
        nres = fid['misfit/norm_weighted'][...]
        nreses.append(nres)
        nrough = fid['regularization/roughening/norm'][...]
        nroughs.append(nrough)

        Bm = fid['Bm'][...]
        slip = Bm[0:-1,:]
        mo, mw = com.moment(slip)
        mos.append(mo)
        mws.append(mw)

        rake = fid['nlin_pars/rake'][...]
        rakes.append(rake)

plt.subplot(311)    
plot_L(nreses, nroughs)
plt.xlim([0.6, 5])

plt.subplot(312)
plt.semilogx(nreses, mos)
plt.xlim([0.6, 5])
plt.grid('on')
plt.ylabel('Moment')

plt.subplot(313)
plt.semilogx(nreses, rakes,'o')
plt.ylabel('rake')
plt.xlabel('weighted residual norm')
plt.xlim([0.6, 5])
plt.grid('on')

plt.savefig('plots/L_curve.png')
plt.show()
