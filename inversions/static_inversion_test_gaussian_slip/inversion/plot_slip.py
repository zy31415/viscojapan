import h5py

from viscojapan.plots import MapPlotFault, plt

for ano in range(30):
    with h5py.File('outs/ano_%02d.h5'%ano,'r') as fid:
        slip = nres = fid['Bm'][...]
        mplt = MapPlotFault('../fault_model/fault_He50km.h5')
        mplt.plot_slip(slip)
        #plt.show()
        plt.savefig('plots/ano_%02d.png'%ano)
        plt.close()
