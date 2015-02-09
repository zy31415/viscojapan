import tempfile

from ..share import file_kur_top, file_kur_contours, file_plate_boundary

__author__ = 'zy'
__all__=['plot_slab_top',
         'plot_slab_contours', 'plot_slab',
         'plot_plate_boundary', 'plot_plate_names',
         ]

def plot_slab_top(gplt,
                  K='',
                  color= '50',
                  lw='thin'):
    gplt.psxy(
        file_kur_top,
        J='', R='', O='', K=K,
        W='%s,%s'%(lw, color),
        )

def plot_slab_contours(gplt, file_contours=file_kur_contours,
                       K='',
                       color='50',
                       lw='thin',
                       label_line = '144/41.5/138/41.5',
                       label_font_size = '9',
                       label_color = 'black',
                       if_contour_annotation = True,
                       ):
    if if_contour_annotation:
        Sq = 'L%s:+Lh+ukm+f%s,%s'%(label_line, label_font_size,label_color)
    else:
        Sq = None

    gplt.psxy(
        file_contours,
        J='', R='', O='', K=K,
        Sq = Sq,
        W='%s,%s,--'%(lw, color)
        )

def plot_slab(gplt, file_contours=file_kur_contours,
              K='', color='50', lw='thin',
              label_line = '144/41.5/138/41.5',
              label_font_size = '9',
              label_color = 'balck',
              if_contour_annotation = True
              ):
    plot_slab_top(gplt, K='', color=color, lw=lw)
    plot_slab_contours(gplt, file_contours=file_contours,
                       K=K, color=color, lw=lw,
                       label_line=label_line,
                       label_font_size = label_font_size,
                       label_color = label_color,
                       if_contour_annotation = if_contour_annotation)


def plot_plate_boundary(gplt,
                        color='red',
                        lw = 'thick',
                        gap = '0.25',
                        ms = '3p',
                        K=''):
    # plot plate boundary
    gplt.psxy(
        file_plate_boundary,
        R = '', J = '', O = '', K=K,
        W='%s,%s'%(lw, color),
        Sf='%s/%s+r+b'%(gap, ms),
        G='%s'%color)


def plot_plate_names(gplt,
                     font_size=12,
                     font_color='yellow',
                     adjust_Pacific = (0,0),
                     adjust_Amurian = (0,0),
                     adjust_Okhotsk = (0,0),
                     adjust_Philippine = (0,0),

                     ):
    pos_Pacific = 146 + adjust_Pacific[0], 34 + adjust_Pacific[1]
    pos_Amurian = 134 + adjust_Amurian[0], 40 + adjust_Amurian[1]
    pos_Okhotsk = 146 + adjust_Okhotsk[0], 45 + adjust_Okhotsk[1]
    pos_Philippine = 138 + adjust_Philippine[0], 31 + adjust_Philippine[1]

    with tempfile.NamedTemporaryFile('w+t') as text:
        text.write('''
{pos_Pacific[0]} {pos_Pacific[1]} Pacific Plate
{pos_Philippine[0]} {pos_Philippine[1]}  Philippine Sea Plate
{pos_Okhotsk[0]} {pos_Okhotsk[1]} Okhotsk Plate
{pos_Amurian[0]} {pos_Amurian[1]} Amurian Plate
'''.format(pos_Pacific = pos_Pacific,
           pos_Amurian = pos_Amurian,
           pos_Okhotsk = pos_Okhotsk,
           pos_Philippine = pos_Philippine,
           )
        )
        text.seek(0,0)
        gplt.pstext(text.name,
                    J='', R='',O='',K='',
                    F='+a0'+'+f{font_size},Helvetica-Bold,{font_color}+jCM'.format(
                        font_size=font_size,
                        font_color = font_color,
                    )
        )
