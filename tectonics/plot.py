import pGMT

gplt = pGMT.GMTPlot()

gplt.psbasemap(
    R = '5/15/52/58',       # region
    J = 'B10/55/55/60/10c', # projection
    B = '4g4',
    K = '')

gplt.pscoast(
    R = '',
    J = '',
    D = 'f',
    W = 'thinnest',
    O = '')


gplt.save('out.pdf')

#gmt.save_shell_script('shell.sh', output_file='>out.ps')
