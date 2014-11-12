import pGMT
import tempfile

import viscojapan as vj

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'FONT_ANNOT_PRIMARY','6')

gplt = pGMT.GMTPlot()

gplt.psbasemap(
    R = '95/160/12/55',       # region
    JB = '127.5/33.5/12/55/19c', # projection
    B = '10g10', U='18/25/0',
    K = '')

# topo
#cpt = '../../share/topo/ETOPO1.cpt'
cpt = 'afrikakarte.cpt'
gmt = pGMT.GMT()
gmt.grdcut(
    '../../share/topo/ETOPO1_Bed_g_gmt4.grd',
    G = 'topo.grd',
    R = '')

gmt = pGMT.GMT()
gmt.grdgradient(
    'topo.grd',
    G = 'topo_grad.grd',
    A = '-70/20',
    R = '')

gplt.grdimage(
    'topo.grd',
    J = '', C=cpt,
    I = 'topo_grad.grd',
    O = '',K = '')

# plot coast
gplt.pscoast(
    R = '', J = '',
    D = 'l', N = 'a/faint,100,-.',
    W = 'faint,50',A='1000',Lf='155/15/35/500+lkm+jt',
    K = '',
    O = '')

# plot plate boundary
vj.gmt.plot_plate_boundary(gplt, color='100')
vj.gmt.plot_Tohoku_focal_mechanism(gplt,scale=0.2)

# plot stations:
# Japan
color = "brown"
gplt.psxy(
    'japan.gmt', S='c0.04',
    R = '', J = '', O = '', K='', W='faint,%s'%color, G=color)

# Korea
gplt.psxy(
    'korea.gmt', S='t0.09',
    R = '', J = '', O = '', K='', W='faint,blue', G='blue')

# China
color = "darkgreen"
gplt.psxy(
    'china.gmt', S='a0.2',
    R = '', J = '', O = '', K='', W='faint,%s'%color, G=color)

# IGS
color = "red"
gplt.psxy(
    'igs.gmt', S='d0.12',
    R = '', J = '', O = '', K='', W='faint,%s'%color, G=color)

# legend
with tempfile.NamedTemporaryFile('w+t') as text:
    text.write('''#
S 0.1i c 0.04 brown faint,brown 0.3i GEONET in Japan
S 0.1i t 0.09 blue faint,blue 0.3i GPS network in Korea
S 0.1i a 0.2 darkgreen faint,darkgreen 0.3i GPS network in China
S 0.1i d 0.12 red faint,red 0.3i IGS stations
''')
    text.seek(0,0)
    gplt.pslegend(
        text.name, R='', J='', O='',
        F='+gazure1', C='0.04i/0.07i', L='1.2',
        D='144/33/3.2/1.5/BL'
        )
    

gplt.save('all_networks_sites.pdf')

gplt.save_shell_script('shell.sh', output_file=' > out.ps')
