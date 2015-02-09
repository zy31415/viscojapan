import tempfile

import pGMT

from ...fault_model import FaultFileReader

from ..share import file_etopo1, topo_cpts

__all__=['plot_vector_legend', 'plot_etopo1']

def plot_vector_legend(gplt,
                       legend_len , scale,
                       lon, lat,
                       text_offset_lon=0, text_offset_lat=0.1):
    # add scale vector
    text = tempfile.NamedTemporaryFile(mode='w+t')
    text.write('%f %f %f 0.'%(lon, lat, legend_len))
    text.seek(0,0)
    gplt.psvelo(
        text.name,
        J='', R='',O='',K='',
        A='0.07i/0.1i/0.1i+a45+g+e+jc',
        Sr='%f/1/0'%scale,G='black',
        W='0.5,black',h='i',
        )
    text.close()

    # add label
    text = tempfile.NamedTemporaryFile(mode='w+t')
    text.write('%f %f %.1fm'%(lon+text_offset_lon, lat+text_offset_lat,legend_len))
    text.seek(0,0)
    gplt.pstext(
        text.name,
        J='', R='',O='',K='',
        F='+f8+jLB',
        )
    text.close()

def plot_etopo1(gplt, A='-70/20', file_topo_cpt=topo_cpts['afrikakarte']):
    gmt = pGMT.GMT()

    file_topo_cut = tempfile.NamedTemporaryFile()
    gmt.grdcut(
        file_etopo1,
        G = file_topo_cut.name,
        R = '')

    gmt = pGMT.GMT()
    file_topo_grad = tempfile.NamedTemporaryFile()
    gmt.grdgradient(
        file_topo_cut.name,
        G = file_topo_grad.name,
        A = A,
        R = '')

    gplt.grdimage(
        file_topo_cut.name,
        J = '', C = file_topo_cpt,
        I = file_topo_grad.name,
        O = '',K = '')

    # close temporary files:
    file_topo_cut.close()
    file_topo_grad.close()



    
