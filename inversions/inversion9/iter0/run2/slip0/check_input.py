from pylab import plt

import viscojapan as vj

reader = vj.EpochalFileReader('incr_slip0_patched.h5')
epochs = reader.get_epochs()

for epoch in epochs:
    slip = reader[epoch].reshape([-1, 35])
    mplt = vj.plots.MapPlotFault('../../fault_model/fault_bott60km.h5')
    mplt.plot_slip(slip)
    plt.show()
    
