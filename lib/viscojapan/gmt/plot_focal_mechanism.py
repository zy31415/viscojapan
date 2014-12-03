import tempfile

from .focal_mechanisms import focal_mechanism_CMT,\
     focal_mechanism_USGS_wphase, focal_mechanism_JMA

__all__ = ['plot_focal_mechanism', 'plot_focal_mechanism_CMT',
           'plot_focal_mechanism_USGS_wphase', 'plot_focal_mechanism_JMA',]

def plot_focal_mechanism(gplt, focal_mechanism, format, scale=0.4,
                         fontsize=8,
                         text_color = 'black',
                         K='', O=''
                         ):
    with tempfile.NamedTemporaryFile('w+t') as text:
        text.write(focal_mechanism.psmeca_str)
        text.seek(0,0)
        gplt.psmeca(text.name,
                    J='', R='',O=O,K=K,T='',L='black', W=text_color,
                    S='%s%f/%f'%(format,scale,fontsize),h='0')

def plot_focal_mechanism_CMT(gplt, scale=0.4, fontsize=8, text_color='black', K='', O='',):
    plot_focal_mechanism(gplt, focal_mechanism_CMT,
                         format = 'm',
                         scale=scale,
                         fontsize = fontsize,
                         text_color = text_color,
                         K=K, O=O)

def plot_focal_mechanism_USGS_wphase(gplt, scale=0.4, fontsize=8, text_color='black', K='', O='',):
    plot_focal_mechanism(gplt, focal_mechanism_USGS_wphase,
                         format = 'm',
                         scale=scale,
                         fontsize = fontsize,
                         text_color = text_color,
                         K=K, O=O)

def plot_focal_mechanism_JMA(gplt, scale=0.4, fontsize=8, text_color='black', K='', O='',):
    plot_focal_mechanism(gplt, focal_mechanism_JMA,
                         format = 'm',
                         scale=scale,
                         fontsize = fontsize,
                         text_color = text_color,
                         K=K, O=O)
