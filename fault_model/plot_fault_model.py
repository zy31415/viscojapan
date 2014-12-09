import pGMT
import viscojapan as vj

plt = vj.gmt.FaultModelPlotter(
    'fault_bott60km.h5')

plt.plot('fault_model_map_view.pdf')
plt.clean()

