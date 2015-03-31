import pGMT
import tempfile

import viscojapan as vj

fault = vj.fm.Fault('../fault_bott80km.h5')

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'FONT_ANNOT_PRIMARY','6',
           'BASEMAP_TYPE','PLAIN')

gplt = gmt.gplt

gplt.psbasemap(
    R = '100/160/20/55',       # region
    JB = '130/37/20/55/19c', # projection
    B = '10', U='18/25/0',
    K = '')


# topo
vj.gmt.plot_etopo1(gplt)

# plot coast
gplt.pscoast(
    R = '', J = '',
    D = 'l', N = 'a/faint,100,-.',
    W = 'faint,50',A='1000',Lf='135/22/35/500+lkm+jt',
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
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'share/co_pred',scale)
plt_vec.plot_vectors(arrow_width='.2', head_length='.1', head_width='.1',
                     pen_width='1.2')
plt_vec.plot_vec_legend(
    lon=133, lat=27,
    leg_len = .01,
    leg_txt = '1 cm pred.',
    text_offset_lon = 0,
    text_offset_lat = -1,
    )

# plot observation
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'share/co_obs',scale,'red')
plt_vec.plot_vectors(arrow_width='.2', head_length='.1', head_width='.1',
                     pen_width='1.2')
plt_vec.plot_vec_legend(
    lon=133, lat=25,
    leg_len = .01,
    leg_txt = '1 cm obs.',
    text_offset_lon = 0,
    text_offset_lat = -1,
    )    

# legend
##with tempfile.NamedTemporaryFile('w+t') as text:
##    text.write('''#
##S 0.3i v 0.25i/0.02i/0.06i/0.05i red red 0.5i 1cm obs.
##S 0.3i v 0.25i/0.02i/0.06i/0.05i black black .5i 1cm pred.
##''')
##    text.seek(0,0)
##    gplt.pslegend(
##        text.name, R='', J='', O='',K='',
##        F='+gazure1', C='0.04i/0.07i', L='1.2',
##        D='102/12.5/4.5/1.25/BL'
##        )
    
gplt.finish()

gmt.save('co_farfield.pdf')






