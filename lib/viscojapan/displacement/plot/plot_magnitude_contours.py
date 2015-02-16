import tempfile

import pGMT
import viscojapan as vj

__all__ = ['MagnitudeContoursPlotter']


class MagnitudeContoursPlotter(object):
    def __init__(self):
        pass

    def plot(self,
             lons, lats, mags,
             output_file,
             if_topo = True
    ):
        gmt = pGMT.GMT()
        gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
                   'LABEL_FONT_SIZE','9',
                   'FONT_ANNOT_PRIMARY','6',
                   'MAP_FRAME_TYPE','plain')

        gplt = gmt.gplt

        north = 60
        south = 12
        east = 190
        west = 100
        gplt.psbasemap(
            R = '{west}/{east}/{south}/{north}'.format(
                west = west,
                east = east,
                south = south,
                north = north),       # region
            JD = '{lon0}/{lat0}/{lat1}/{lat2}/{wid}'\
            .format(lon0 = vj.TOHOKU_EPICENTER[0],
                    lat0 = vj.TOHOKU_EPICENTER[1],
                    lat1 = south,
                    lat2 = north,
                    wid = '9i',
                    ), # projection
            B = '20', U='18/25/0',
            K = '')

        # topo
        if if_topo:
            vj.gmt.plot_etopo1(gplt)

        with tempfile.NamedTemporaryFile('w+t') as fid:
            self._write_to_temp_file(fid, lons, lats, mags)

            pltxyz = vj.gmt.GMTXYZ(
                gmt,
                file_xyz = fid.name,
                if_log_color_scale = True,
                cpt_scale = '-3.1/0.6/0.001',
                interp_inc = '40k',
                interp_searching_radius = '10',
                )
            #pltxyz.maskout_water(A='1000k',D='h')
            #pltxyz.plot_xyz()
            pltxyz.plot_contour(
                contours=[0.001, 0.0026, 0.005,0.01,0.1,0.2],
                W='thick,red',
                label_line = 'L142.37/38.30/80/60,142.37/38.30/90/20,142.37/38.30/-160/40,158/38.30/180/5',
                label_font_size = 8,
                smooth_factor = 100,
                )


        #pltxyz.plot_scale(x=15, y=8)


        # plot coast
        gplt.pscoast(
            R = '', J = '',
            D = 'h', N = 'a/faint,100,-.',
            W = 'faint,50',A='5000',Lf='180/15/35/500+lkm+jt',
            K = '',
            O = '')

        # plot plate boundary
        vj.gmt.plot_plate_boundary(gplt, color='100')
        vj.gmt.plot_focal_mechanism_JMA(gplt,scale=0.2, fontsize=0)
        gplt.finish()

        gmt.save(output_file)

    def _write_to_temp_file(self, fid, lons, lats, mags):
        for lon, lat, mag in zip(lons, lats, mags):
            fid.write('%f %f %f\n'%(lon, lat, mag))
        fid.seek(0)


