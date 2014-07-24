import viscojapan as vj

f1 = vj.EpochalG('../G_Rake66.h5')
G1 = f1[0]

f2 = vj.EpochalG('../G_Rake90.h5')
G2 = f2[0]

f3 = vj.EpochalG('../G_Rake95.h5')
G3 = f3[0]

fno = 285

bm = vj.MyBasemap(
    region_code = 'near')
scale = 2e-2
mplt = vj.MapPlotDisplacement(basemap = bm)
mplt.plot_disp(G1[:,fno],f1.sites, scale= scale)
mplt.plot_disp(G2[:,fno],f2.sites, scale= scale,color='red')
mplt.plot_disp(G3[:,fno],f3.sites, scale= scale,color='blue')

vj.MapPlotFault('../fault_He50km.h5',basemap = bm).plot_fault(fno)

vj.plt.show()
