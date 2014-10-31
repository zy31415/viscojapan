import h5py

from viscojapan.plots import MapPlotFault, plt
import viscojapan as vj

fault_file = '../../fault_model/fault_bott60km.h5'
earth_file = 'earth.model_He63km_VisM1.0E19'
for ano in range(30):
    with h5py.File('outs/ano_%02d.h5'%ano,'r') as fid:
        Bm = nres = fid['Bm'][...]
        slip = Bm[0:-1]
        mplt = MapPlotFault(fault_file)
        mplt.plot_slip(slip)

        mplt = vj.plots.MapPlotSlab()
        mplt.plot_top()

        mo, mw = vj.ComputeMoment(fault_file, earth_file).moment(slip)

        plt.title('Mo = %.5g, Mw = %.4f'%(mo, mw))
        #plt.show()
        plt.savefig('plots/ano_%02d.pdf'%ano)
        plt.close()
