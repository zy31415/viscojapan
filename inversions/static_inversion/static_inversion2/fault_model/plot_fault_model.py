import pGMT
import viscojapan as vj

plt = vj.gmt.FaultModelPlotter(
    'fault_bott60km.h5')

plt.plot()
plt.plot_seafloor(
    network='SEAFLOOR_CO',
    justification = 'TM',
    text_offset_Y = -0.12,
    text_offset_X = -0.1,
    )
plt.save('fault_model_map_view_60km.pdf')

