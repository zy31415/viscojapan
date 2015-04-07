import viscojapan as vj

file1 = '../G0_He50km_VisM6.3E18_Rake83.h5'
file2 = '../../../../inversion10/iter2_corr/green_function/G0_He50km_VisM6.3E18_Rake83.h5'
file3 = '../../../../inversion10/iter2/green_function/G0_He50km_VisM6.3E18_Rake83.h5'


def get_ts(site, nth_subflt, file):
    g1 = vj.inv.ep.EpochG(file)
    
    y1 = g1.cumu_ts(site,'e',nth_subflt)
    t1 = g1.get_epochs()

    return y1, t1

site = 'J550'
nth_subflt = 150

y1, t1 = get_ts(site, nth_subflt, file1)
y2, t2 = get_ts(site, nth_subflt, file2)
y3, t3 = get_ts(site, nth_subflt, file3)

from pylab import plt

plt.plot(t1, y1, 'x-',label='gravity')
plt.plot(t2, y2, 'o-',label='non-gravity')
plt.plot(t3, y3, '>-',label='non-gravity-depfac4')

plt.legend()
plt.show()
