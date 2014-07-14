from numpy import arange, frompyfunc, asarray, linspace, mean

from viscojapan.utils import my_vectorize


class CubicBSplines(object):
    def __init__(self, ds):
        self.ds = ds

    def _b_spline_scalar(self,s):
        ds = self.ds

        if s < -3.*ds and s >= -4.*ds:
            y = (s + 4.*ds)**3
        elif s < -2.*ds and s >= -3.*ds:
            y = ((s + 4.*ds)**2)*(-2.*ds - s) + \
                (s + 4.*ds)*(s + 3.*ds)*( -ds - s) + \
                (-s)*(s + 3.*ds)**2
        elif s < -ds and s >= -2.*ds:
            y = (s + 4.*ds) * (-ds - s)**2 + \
                (-s)*(s + 3.*ds)*( -ds - s) + \
                (s**2)*(s + 2.*ds)
        elif s < 0  and s >= -ds:
            y = (-s)**3
        else:
            y = 0.
        return y/4./(ds**3)

    def b_spline(self, s):
        fn_vec = frompyfunc(self._b_spline_scalar, 1, 1)
        res = fn_vec(asarray(s - 2.*self.ds, float))
        return asarray(res, float)

    def b_spline_average_over_sections(self, j, s):
        res = []
        for s1, s2 in zip(s[0:-1], s[1:]):
            inter_s = linspace(s1, s2, 50)
            out = self.b_spline(j, inter_s)
            res.append(mean(out))
        return asarray(res)
            
            
        
if __name__ == '__main__':
    from pylab import plt

    func = CubicBSplines(ds=50)
    
    s = arange(-150, 150, 1)

    y = func.b_spline(s)

    plt.plot(s,y,color='red')

    plt.show()

