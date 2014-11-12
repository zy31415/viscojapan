from subprocess import check_call
import tempfile

import pGMT
import viscojapan as vj

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'FONT_ANNOT_PRIMARY','6',
           'MAP_FRAME_TYPE','plain')

gplt = pGMT.GMTPlot()

gplt.psbasemap(
    R = '140/145/35/41.5',       # region
    JB = '142.5/38.5/35/41.5/14c', # projection
    B = '2', U='18/25/0',
    P='',K='',
    )

vj.gmt.plot_etopo1(gplt, A='-80/10',
                   file_topo_cpt=vj.gmt.topo_cpts['afrikakarte'])

I = '5k'
gmt = pGMT.GMT()
gmt.nearneighbor(
    'coseismic_slip.txt',
    G='~coseismic_slip.grd', I=I, N='8', R='', S='100k'
    )
gmt.grdclip(
    '~coseismic_slip.grd',
    G='~coseismic_slip_low_cut.grd',
    Sb='1/NaN')

gmt = pGMT.GMT()
##gmt.makecpt(
##    C='temperature.cpt',
##    T='0/70/0.1',M='')
gmt.grd2cpt(
    '~coseismic_slip.grd',
    #C='temperature.cpt',
    C='no_green',
    Z=''
    )
gmt.save_stdout('~mag.cpt')


gmt.grdsample(
    '~topo_grad.grd',
    G='~topo_grad_resampled.grd', I=I)

# cut out slip that is out of trench
gmt.grdmask(
    vj.gmt.file_kur_top,
    G='~plate_boundary_mask_file.grd',A='',
    N='1/1/NaN',
    I=I,R=''
    )

gmt.grdmath(
    '~coseismic_slip_low_cut.grd',
    '~plate_boundary_mask_file.grd',
    'OR',
    '= ~mag.grd')

gmt.grdlandmask(R='', Dh='', I=I,
                N='1/NaN',G='~sea_mask.grd')
check_call("gmt grdmath ~mag.grd ~sea_mask.grd OR = ~mag.grd",
           shell=True)

gplt.grdimage(
    '~mag.grd', J='', R='',
    C='~mag.cpt',O='',K='', G='', Q='',
    I = '~topo_grad_resampled.grd',
    )

with tempfile.NamedTemporaryFile('w+t') as fid:
    fid.write('''
5 A
10 A 
20 A 
40 A
60 A
''')
    fid.seek(0,0)
    gplt.grdcontour(
        '~mag.grd', C=fid.name, A='1+f9+um',
        G='n1/.5c', J='', R='', O='',K='', W='thick'
        )

# plot coast
gplt.pscoast(
    R = '', J = '',
    D = 'l', N = 'a/faint,100,-.',
    W = 'faint,50',A='1000',Lf='155/15/35/500+lkm+jt',
    O = '', K='')

##gplt.psscale(
##    D='0.3/12.5/4c/.2c',
##    Baf='::/:m:', O='',K='',
##    C='~mag.cpt')

# legend
with tempfile.NamedTemporaryFile('w+t') as text:
    text.write('''#
B ~mag.cpt 0.1 0.2 -Baf::/:m:
''')
    text.seek(0,0)
    gplt.pslegend(
        text.name, R='', J='', O='', K='',
        F='+gazure1', C='0.04i/0.07i', L='1.2',
        D='143.5/35.2/4/1.2/BL'
        )

# plot plate boundary
vj.gmt.plot_plate_boundary(gplt)
# plot focal mechanism
vj.gmt.plot_Tohoku_focal_mechanism(gplt,scale=0.4, K=None)

gplt.save('inverted_coseismic_slip.pdf')

gplt.save_shell_script('shell.sh', output_file=' > out.ps')
