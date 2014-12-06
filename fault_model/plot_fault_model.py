import pGMT
import viscojapan as vj

plt = vj.gmt.FaultModelPlotter(
    'fault_bott60km.h5')

plt.plot('fault_model.pdf')


##gmt = pGMT.GMT()
##gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
##           'LABEL_FONT_SIZE','9',
##           'MAP_FRAME_TYPE','plain',
##           )
##
##gplt = gmt.gplt
##
##gplt.psbasemap(
##    R = '138/146/33.5/42',       # region
##    J = 'B141.5/38.5/33.5/42/15c', # projection
##    B = '2', U='20/0/22/Yang', P='', K=''
##    )
##
##vj.gmt.plot_etopo1(gplt)
##
##vj.gmt.plot_slab(gplt, file_contours='../share/slab1.0/kur_contours_above_100km.in')
##
##gplt.pscoast(
##    R = '', J = '',
##    D = 'h', N = 'a/faint,50,--',
##    W = 'faint,100', L='f145/34/38/100+lkm+jt',
##    O = '', K='')
##
##vj.gmt.plot_fault_model(gplt,'fault_bott60km.h5')
##
##vj.gmt.plot_seafloor_stations(gplt, marker_size=0.4,color='red')
##vj.gmt.plot_GEONET_Japan_stations(gplt, color='red')
##
##vj.gmt.plot_focal_mechanism_USGS_wphase(gplt,K=None)
##
##gmt.save('fault_model_map_view.pdf')
##gmt.save_shell_script('shell.sh', output_file=' > out.ps')
