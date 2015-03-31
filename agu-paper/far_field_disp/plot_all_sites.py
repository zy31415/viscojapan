import pGMT
import tempfile

import viscojapan as vj

fault = vj.fm.Fault('fault_bott80km.h5')

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'FONT_ANNOT_PRIMARY','6')

gplt = gmt.gplt

gplt.psbasemap(
    R = '100/160/12/55',       # region
    JB = '130/33.5/12/55/19c', # projection
    B = '10g10', U='18/25/0',
    K = '')


# topo
#vj.gmt.plot_etopo1(gplt)

# plot coast
gplt.pscoast(
    R = '', J = '',
    D = 'l', N = 'a/faint,100,-.',
    W = 'faint,50',A='1000',Lf='155/15/35/500+lkm+jt',
    K = '',
    O = '')

# plot plate boundary
vj.gmt.plot_plate_boundary(gplt, color='100')

vj.fm.gmt_plot.gplt_marking_dip_change_on_fault_meshes(
    gplt, fault,
    width='thick'
    )
vj.gmt.plot_focal_mechanism_USGS_wphase(gplt,scale=0.2, fontsize=0)

scale = 120

# plot prediction
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'share/post_1344_pred',scale)
plt_vec.plot_vectors(arrow_width='.2', head_length='.1', head_width='.1',
                     pen_width='1.2')
plt_vec.plot_vec_legend(
    lon=143.5, lat=52,
    leg_len = .01,
    leg_txt = '1 cm pred. ONSHORE',
    text_offset_lon = -0.2,
    text_offset_lat = -0.11,
    )

# plot observation
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'share/post_1344_obs',scale,'red')
plt_vec.plot_vectors(arrow_width='.2', head_length='.1', head_width='.1',
                     pen_width='1.2')
plt_vec.plot_vec_legend(
    lon=143.5, lat=48,
    leg_len = .01,
    leg_txt = '1 cm obs. ONSHORE',
    text_offset_lon = -0.2,
    text_offset_lat = -0.11,
    )    

### IGS
##color_IGS = "red"
##gplt.psxy(
##    'sites_files/igs.gmt', S='d0.16',
##    R = '', J = '', O = '', K='', W='faint,%s'%color_IGS, G=color_IGS)
##
##vj.gmt.plot_plate_names(gplt,
##                        font_size = 12,
##                        font_color='yellow',
##                        adjust_Pacific = (5,2),
##                        adjust_Amurian = (-1.5,-0.5),
##                        adjust_Okhotsk = (3,3),
##                        adjust_Philippine = (-2,-5)
##                        )



### legend
##with tempfile.NamedTemporaryFile('w+t') as text:
##    text.write('''#
##S 0.1i c 0.08 {color_EXP} faint,{color_EXP} 0.3i GEONET in Japan (Model EXP)
##S 0.1i c 0.08 {color_2EXPs} faint,{color_2EXPs} 0.3i GEONET in Japan (Model 2EXPs)
##S 0.1i d 0.16 {color_IGS} faint,{color_IGS} 0.3i IGS stations
##'''.format(color_EXP = color_EXP,
##           color_2EXPs = color_2EXPs,
##           color_IGS = color_IGS))
##    text.seek(0,0)
##    gplt.pslegend(
##        text.name, R='', J='', O='',K='',
##        F='+gazure1', C='0.04i/0.07i', L='1.2',
##        D='102/12.5/4.5/1.25/BL'
##        )
##    
gplt.finish()

gmt.save('all_networks_sites.pdf')






