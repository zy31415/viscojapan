
from numpy import arange, asarray

from b_splines import CubicBSpline

class BasisMatrix(object):
    def __init__(self):

        stk_sj = arange(0, 740, 20)
        dip_sj = arange(0,260, 20)

        stk_spl = CubicBSpline(stk_sj)
        dip_spl = CubicBSpline(dip_sj)

        for n in range(11):
            for m in range(35):
                x_slip = asarray([stk_spl(m, stk_sj)], float)
                y_slip = asarray([dip_spl(n, dip_sj)], flaot)

                slip = dot(x_slip.T, y_slip)
                

                

        
        
