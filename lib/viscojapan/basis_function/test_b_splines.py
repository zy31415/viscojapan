from numpy import arange, frompyfunc, asarray
from pylab import plt

from viscojapan.utils import my_vectorize


class CubicBSpline(object):
    def __init__(self, sj):        
        self.sj = asarray(sj, float)
        self.ds = self.sj[1] - self.sj[0]

    def _b_spline_scalar(self, j, s):
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
        j = j + 2
        fn_vec = frompyfunc(lambda s: self._b_spline_scalar(j, s-self.ds/2.), 1, 1)
        res = fn_vec(asarray(s, float))
        return asarray(res, float)
    

sj = arange(0, 700, 50)

func = CubicBSpline(sj=sj)

s = arange(0,700,0.5)

y = func.b_spline(12,s)

plt.plot(s,y)

for ii in sj:
    plt.axvline(ii, color='grey', ls='--')
plt.show()

