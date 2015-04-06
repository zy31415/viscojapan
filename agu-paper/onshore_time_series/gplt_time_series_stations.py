import pGMT
import viscojapan as vj

sites_names = ['J162', 'J059', 'CHAN']
sites = vj.sites_db.SitesDB().gets(sites_names)

gmt = pGMT.GMT()

gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'FONT_ANNOT_PRIMARY','6',
           'MAP_FRAME_TYPE','plain')

gplt = gmt.gplt

lon1 = 115
lon2 = 150
lat1 = 30
lat2 = 50

gplt.psbasemap(
    R = '{lon1}/{lon2}/{lat1}/{lat2}'.format(lon1=lon1,
                                     lon2=lon2,
                                     lat1 = lat1,
                                     lat2 = lat2
                                     ),       # region
    J = 'B{lon0}/{lat0}/{lat1}/{lat2}/14c'.format(
        lon0=(lon1+lon2)/2.,
        lat0 = (lat1+lat2)/2.,
        lat1 = lat1,
        lat2 = lat2), # projection
    B = '5', U='18/25/0',
    P='',K='',
    )

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,150,-.',
    W = 'faint,dimgray',A='500',L='100/26/38/200+lkm+jt',
    O = '', K='')

vj.gmt.plot_stations(
    gplt, sites,
    S = 's.2',
    color = 'red',
    fill_color = 'red',
    fontcolor = 'blue',
    fontsize = 16,
    text_offset_X = -.5,
    text_offset_Y = 1,
    )

vj.gmt.plot_focal_mechanism_JMA(gplt, scale=.2, fontsize=0)

gplt.finish()
gmt.save('time_series_stations.pdf')
