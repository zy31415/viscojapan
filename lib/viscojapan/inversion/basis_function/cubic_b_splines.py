from numpy import arange, frompyfunc, asarray

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

    def b_spline_over_sections(self, sj, j):
        sms = []
        for s1, s2 in zip(sj[0:-1],sj[1:]):
            sm = (s1+s2)/2.
            sms.append(sm)

        sms = asarray(sms)

        y = self.b_spline(sms-sms[j])

        return sms, y        
            
            
        
if __name__ == '__main__':
    from pylab import plt
    ds = 20
    func = CubicBSplines(ds=ds)


    s = arange(0, 701, 20)
    sm, y = func.b_spline_over_sections(s,30)
    plt.plot(sm,y,color='red',marker='o')

    for si in s:
        plt.axvline(si, color='gray')

    plt.show()

