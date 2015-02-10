import pGMT
import viscojapan as vj

fault = vj.fm.Fault('fault_bott80km.h5')

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'MAP_FRAME_TYPE','plain',
           )

gplt = gmt.gplt


vj.fm.gmt_plot.gplt_mark_dip_change_on_fault_meshes(gplt, fault)
