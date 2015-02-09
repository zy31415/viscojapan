import pGMT
import viscojapan as vj


def plot_seafloor(gplt,
                  network='SEAFLOOR',
              justification='TR',
              text_offset_X = 0,
              text_offset_Y = 0,
              ):
    vj.gmt.plot_seafloor_stations(gplt, marker_size=0.5,color='red',
                           network=network,
                           justification = justification,
                           text_offset_X = text_offset_X,
                           text_offset_Y = text_offset_Y)

fault = vj.fm.Fault('fault_bott80km.h5')

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'MAP_FRAME_TYPE','plain',
           )

gplt = gmt.gplt

gplt.psbasemap(
    R = '138/146/33.5/42',       # region
    J = 'B141.5/38.5/33.5/42/15c', # projection
    B = '2', U='20/0/22/Yang', P='', K=''
    )

vj.gmt.plot_etopo1(gplt)
vj.gmt.plot_slab(gplt)

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,50,--',
    W = 'faint,100', L='f145/34/38/100+lkm+jt',
    O = '', K='')

vj.fm.gmt_plot.gplt_fault_model(gplt, fault)

vj.gmt.plot_GEONET_Japan_stations(gplt, color='red')

plot_seafloor(
    gplt,              
    network = 'SEAFLOOR_POST',    
    text_offset_X = -0.1,
    text_offset_Y = -0.1
    )

vj.gmt.plot_focal_mechanism_USGS_wphase(
    gplt,
    fontsize = 0)

gplt.finish()

gmt.save('fault_model.pdf')



