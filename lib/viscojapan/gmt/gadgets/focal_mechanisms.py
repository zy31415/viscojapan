__all__ = ['focal_mechanism_CMT','focal_mechanism_USGS_wphase','focal_mechanism_JMA']

class FocalMechanism(object):
    def __init__(self):
        pass
        

focal_mechanism_CMT = FocalMechanism()

focal_mechanism_CMT.lon = 143.05
focal_mechanism_CMT.lat = 37.52
focal_mechanism_CMT.dep = 20.
focal_mechanism_CMT.strike1 = 203
focal_mechanism_CMT.dip1 = 10
focal_mechanism_CMT.slip1 = 88

focal_mechanism_CMT.strike2 = 25
focal_mechanism_CMT.dip2 = 80
focal_mechanism_CMT.slip2 = 90
focal_mechanism_CMT.moment = 9.1
focal_mechanism_CMT.source_name = 'Harvard Global CMT'
focal_mechanism_CMT.__str__ = '''Harvard Global CMT focal mechanism.
Found it at:
http://www.globalcmt.org/CMTsearch.html
'''
focal_mechanism_CMT.psmeca_str = '143.05 37.52 20 1.73 -0.28 -1.45 2.12 4.55 -0.66 29 0 0 CMT'


focal_mechanism_USGS_wphase = FocalMechanism()
focal_mechanism_USGS_wphase.psmeca_str = '142.369 38.321 24 1.82 -0.13 -1.69 1.34 3.17 -.56 29 0 0 USGS wphase'
focal_mechanism_USGS_wphase.__str__ ='''USGS WPhase Moment Solution
Found it at USGS website:
http://earthquake.usgs.gov/earthquakes/eqinthenews/2011/usc0001xgp/neic_c0001xgp_wmt.php
'''

focal_mechanism_JMA = FocalMechanism()
focal_mechanism_JMA.lon = 142 + 51.6/60.
focal_mechanism_JMA.lat = 38 + 6.2/60.
focal_mechanism_JMA.psmeca_str = '%f %f 24 1.82 -0.13 -1.69 1.34 3.17 -.56 29 0 0 USGS wphase'%\
                                 (focal_mechanism_JMA.lon, focal_mechanism_JMA.lat)
focal_mechanism_JMA.__str__ ='''JMA
JMA solution:
http://www.jma.go.jp/jma/en/2011_Earthquake/Information_on_2011_Earthquake.html

Note that only Hypocenter data are JMA.
The moment machanisms is from USGS wphase.

'''
