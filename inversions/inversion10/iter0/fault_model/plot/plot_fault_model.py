import pGMT
import viscojapan as vj

dep = 120
plt = vj.gmt.FaultModelPlotter(
    '../fault_bott%dkm.h5'%dep
    )
plt.plot('fault_model_map_view_%dkm.pdf'%dep)
plt.clean()

