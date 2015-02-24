import pGMT
import viscojapan as vj

dep = 120
plt = vj.fm.gmt_plot.FaultModelPlotter(
    '../fault_bott%dkm.h5'%dep
    )
plt.plot()
plt.save('fault_model_map_view_%dkm.pdf'%dep)

