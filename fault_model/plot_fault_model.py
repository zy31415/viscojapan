import pGMT
import viscojapan as vj

plt = vj.gmt.FaultModelPlotter(
    'fault_bott80km.h5')

plt.plot()
plt.plot_seafloor(
    network='SEAFLOOR',
    justification='TR',
    text_offset_X = 0,
    text_offset_Y = 0,
    )

plt.save('fault_model_map_view.pdf')


