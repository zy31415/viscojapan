import tempfile

__all__ = ['VecFieldPlotter']

class VecFieldPlotter(object):
    def __init__(self,
                 gmt,
                 vec_file,
                 scale,
                 color='black'
                 ):
        self.gmt = gmt
        self.gplt = gmt.gplt

        self.vec_file = vec_file

        self.scale = scale

        self.color = color

    def plot_vectors(self,
                     arrow_width = '0.03i',
                     head_length = '0.1i',
                     head_width = '0.1i'):
        self.gplt.psvelo(
            self.vec_file,
            J='', R='',O='',K='',
            A = '{arrow_width}/{head_length}/{head_width}+a45+g+e'.format(
                arrow_width = arrow_width,
                head_length = head_length,
                head_width = head_width,
                ),
            Sr = '%s/1/0'%self.scale,
            G = self.color,
            W = '0.5,%s'%self.color,
            h='i',
            )

    def plot_vec_legend(
        self,
        lon,
        lat,
        leg_len,
        leg_txt,
        text_offset_lon = 0.1,
        text_offset_lat = 0.1,
        arrow_width = '0.03i',
        head_length = '0.1i',
        head_width = '0.1i'
        ):
        with tempfile.NamedTemporaryFile(mode='w+t') as text:
            text.write('%f %f %f 0.'%(lon, lat, leg_len))
            text.seek(0,0)
            self.gplt.psvelo(
                text.name,
                J='', R='',O='',K='',
                A='{arrow_width}/{head_length}/{head_width}+a45+g+e+jc'.format(
                arrow_width = arrow_width,
                head_length = head_length,
                head_width = head_width,
                ),
                Sr = '%f/1/0'%self.scale,
                G = self.color,
                W = '0.5,%s'%self.color,
                h='i',
                )

        with tempfile.NamedTemporaryFile(mode='w+t') as text:
            text.write('%f %f %s'%(lon+text_offset_lon, lat+text_offset_lat,
                                   leg_txt))
            text.seek(0,0)
            self.gplt.pstext(
                text.name,
                J='', R='',O='',K='',
                F='+f8+jLB',
                )

