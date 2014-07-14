from numpy import arange, frompyfunc, asarray, linspace, mean
from pylab import plt

from viscojapan.utils import my_vectorize


class CubicBSpline(object):
    def __init__(self, sj):        
        self.sj = asarray(sj, float)
        self.ds = self.sj[1] - self.sj[0]

    def _b_spline_scalar(self, j, s):
        j = j + 2
        sj = self.sj
        ds = self.ds

        if s < (sj[j] - 3.*ds) and s >= (sj[j] - 4.*ds):
            y = (s - sj[j] + 4.*ds)**3
        elif s < (sj[j] - 2.*ds) and s >= (sj[j] - 3.*ds):
            y = ((s - sj[j] + 4.*ds)**2)*(sj[j] - 2.*ds - s) + \
                (s - sj[j] + 4.*ds)*(s - sj[j] + 3.*ds)*(sj[j] - ds - s) + \
                (sj[j] - s)*(s - sj[j] + 3.*ds)**2
        elif s < (sj[j] - ds) and s >= (sj[j] - 2.*ds):
            y = (s - sj[j] + 4.*ds) * (sj[j] - ds - s)**2 + \
                (sj[j] - s)*(s - sj[j] + 3.*ds)*(sj[j] - ds - s) + \
                ((sj[j] - s)**2)*(s - sj[j] + 2.*ds)
        elif s < sj[j] and s >= (sj[j] - ds):
            y = (sj[j] - s)**3
        else:
            y = 0.
        return y/4./(ds**3)

    def b_spline(self, j, s):        
        fn_vec = frompyfunc(lambda s: self._b_spline_scalar(j, s-self.ds/2.), 1, 1)
        res = fn_vec(asarray(s, float))
        return asarray(res, float)

    def b_spline_average_over_sections(self, j, s):
        res = []
        for s1, s2 in zip(s[0:-1], s[1:]):
            inter_s = linspace(s1, s2, 50)
            out = self.b_spline(j, inter_s)
            res.append(mean(out))
        return asarray(res)
            
            
        
if __name__ == '__main__':
        

    sj = arange(0, 740, 50)

    sj_dense = arange(0, 740, 1)

    func = CubicBSpline(sj=sj)

    s = arange(0,700,50)

    y1  = func.b_spline_average_over_sections(5, s)


    y2 = func.b_spline(5,sj_dense)

    plt.plot((s[1:]+s[0:-1])/2,y1, marker='o')
    plt.plot(sj_dense,y2,color='red')

    for ii in sj:
        plt.axvline(ii, color='grey', ls='--')
    plt.show()

