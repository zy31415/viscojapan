import pGMT
import tempfile

cpt = '../../share/topo/ETOPO1.cpt'

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9')

gplt = pGMT.GMTPlot()

gplt.psbasemap(
    R = '128/150/30/46',       # region
    J = 'B140/38/28/48/18c', # projection
    B = '4g4', U='18/25/0',
    K = '')

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

gplt.pscoast(
    R = '', J = '',
    D = 'l', N = 'a/faint,50,--',
    W = 'faint,30',A='1000',L='f146/32/38/200+lkm+jt',
    K = '',
    O = '')

# plot plate boundary
gplt.psxy(
    'share/plate_boundary_PB/PB2002_boundaries.gmt',
    R = '', J = '', O = '', K='', W='thick,red',
    Sf='0.25/3p', G='red')

# Plot relative plate motion vector
text = tempfile.NamedTemporaryFile('w+t')
text.write('146.5 37 -70 1')
text.seek(0,0)
gplt.psxy(text.name,
          J='', R='',O='',K='',
          S='V0.15i/0.15i/0.4i+a100+g+e',G='red',
          W='5, red',
          )
text.close()

# Plot label 78mm/yr
text = tempfile.NamedTemporaryFile('w+t')
text.write('''146.5 36.5 78mm/yr''')
text.seek(0,0)
gplt.pstext(text.name,
            J='', R='',O='',K='',
            F='+a0'+'+f10,Helvetica,red'+'+jCM')
text.close()

# Plot label Japan Trench
text = tempfile.NamedTemporaryFile('w+t')
text.write('144.5 37.3 Japan Trench')
text.seek(0,0)
gplt.pstext(text.name,
            J='', R='',O='',K='',
            F='+a70'+'+f10,Helvetica-Bold,black'+'+jCM')
text.close()

# Plot label Plates Names
text = tempfile.NamedTemporaryFile('w+t')
text.write('''146 34 Pacific Plate
138 31 Philippine Sea Plate
146 45 Okhotsk Plate
134 40 Amuria Plate
''')
text.seek(0,0)
gplt.pstext(text.name,
            J='', R='',O='',K='',
            F='+a0'+'+f12,Helvetica-Bold,yellow'+'+jCM')
text.close()

# Plot focal mechanism
text = tempfile.NamedTemporaryFile('w+t')
text.write('''lon lat depth str dip slip st dip slip mant exp plon plat
143.05, 37.52 20. 203 10 88 25 80 90  9.1 0 0 0
''')
text.seek(0,0)
gplt.psmeca(text.name,
            J='', R='',O='',K='',
            S='c0.4',h='1')
text.close()

gplt.psscale(D='10/-1/6/.4h', B='af', C=cpt,O='',)

gplt.save('tectonics.pdf')

gplt.save_shell_script('shell.sh', output_file=' > out.ps')
