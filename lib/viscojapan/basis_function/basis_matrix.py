
from numpy import arange, asarray, dot

from viscojapan.plots import MapPlotFault, plt

from b_splines import CubicBSpline

class BasisMatrix(object):
    def __init__(self):

        stk_sj = arange(0, 741, 20)
        stk_sj1 = arange(0, 701, 20)
        dip_sj = arange(0,261, 20)
        dip_sj1 = arange(0,221, 20)

        stk_spl = CubicBSpline(stk_sj)
        dip_spl = CubicBSpline(dip_sj)

        for n in range(11):
            for m in range(35):
                x_slip = asarray([stk_spl.b_spline_average_over_sections(m, stk_sj1)], float)
                y_slip = asarray([dip_spl.b_spline_average_over_sections(n, dip_sj1)], float)

                slip = dot(y_slip.T, x_slip)
                mplt = MapPlotFault('/home/zy/workspace/viscojapan/inversions/static_inversion/coseismic_inversion_wider/fault_model/fault_He50km_east.h5')
                mplt.plot_slip(slip.flatten())
                plt.show()
                
b = BasisMatrix()
                

        
        
