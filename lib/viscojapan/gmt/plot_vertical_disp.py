import pGMT
from .utils import topo_cpts

__all__ = ['GMTVerticalDisp']

class GMTVerticalDisp(object):
    def __init__(self, gplt, file_vertical_disp):
        self.gplt = gplt
        self.file_vertical_disp = file_vertical_disp

    def plot(self):
        gmt = pGMT.GMT()
        gmt.nearneighbor(
            self.file_vertical_disp,
            G='~grd', I='1k', N='8', R='', S='60k'
            )

        gmt = pGMT.GMT()
        gmt.makecpt(C=topo_cpts['seminf-haxby'],
                    T='-4/-0.1/0.1',Q='',M='')
        gmt.save_stdout('~cpt')

        self.gplt.grdimage(
            '~grd',
            J='', R='', C='~cpt',O='',K='', Q='',
            )
        
        # fill water with white color
        self.gplt.pscoast(R='', J='', S='white', O='', K='')
        

    
