__all__ = ['focal_mechanism_CMT']

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
Found it at USGS website:
http://www.globalcmt.org/CMTsearch.html
'''
focal_mechanism_CMT.psmeca_str = '143.05 37.52 20 1.73 -0.28 -1.45 2.12 4.55 -0.66 29 X Y '
