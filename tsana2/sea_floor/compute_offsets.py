from datetime import date

from pyproj import Geod
from numpy import sin, cos, pi, asarray

sites = ['KAMN', 'KAMS', 'MYGI', 'MYGW', 'FUKU']
lons1 = asarray([143. + 21./60. + 43.869/3600.,
        143. + 15./60. + 48.021/3600.,
        142. + 54./60. + 59.881/3600.,
        142. + 25./60. + 59.327/3600.,
        142. + 4./60. + 51.233/3600.,
        ], float)

lons2 = asarray([143. + 21./60. + 44.443/3600.,
        143. + 15./60. + 48.893/3600.,
        142. + 55./60. + 0.788/3600.,
        142. + 25./60. + 59.919/3600.,
        142. + 4./60. + 51.412/3600.,
        ], float)

lats1 = asarray([38. + 53./60. + 16.740/3600.,
        38. + 38./60. + 11.271/3600.,
        38. + 4./60. + 51.388/3600.,
        38. + 8./60. + 55.897/3600.,
        37. + 9./60. + 58.002/3600.,
        ], float)

lats2 = asarray([38. + 53./60. + 16.551/3600.,
        38. + 38./60. + 10.981/3600.,
        38. + 4./60. + 51.051/3600.,
        38. + 8./60. + 55.734/3600.,
        37. + 9./60. + 57.948/3600.,
        ], float)

heis1 = [-2306.51,
        -2193.21,
        -1645.83,
        -1044.71,
        -1209.47,
        ]

heis2 = [-2304.90,
        -2191.72,
        -1642.69,
        -1045.49,
        -1208.61,
        ]

date_of_obs = asarray([date(2011, 4, 3),
               date(2011, 4, 5),
               date(2011, 3, 28),
               date(2011, 3, 27),
               date(2011, 3, 29),
               ])

date_eq = date(2011,3,11)

days = [ii.days for ii in date_of_obs - date_eq]

g = Geod(ellps='WGS84')
az12,az21,dist = g.inv(lons1, lats1, lons2, lats2)

eastings = dist*sin(asarray(az12)*pi/180.)
northings = dist*cos(asarray(az12)*pi/180.)
upings = asarray(heis2) - asarray(heis1)

disp_dic = {site:((loni, lati),day,(e,n,u)) for site, loni, lati, day, e, n, u in \
            zip(sites, lons1, lats1, days, eastings, northings, upings)}

with open('sites_seafloor','wt') as fid:
    fid.write('# site  lon  lat  easting  northing  uping  day\n')
    for key in sorted(disp_dic):
        pos, day, disp = disp_dic[key]
        fid.write('%s %f %f %f %f %f %d\n'%\
                  (key, pos[0], pos[1], disp[0], disp[1], disp[2], day))
    
    
