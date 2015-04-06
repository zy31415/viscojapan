import viscojapan as vj

file1 = '../G0_He50km_VisM6.3E18_Rake83.h5'
file2 = '../../../../inversion10/iter2/green_function/G0_He50km_VisM6.3E18_Rake83.h5'


site = 'J550'
nth_subflt = 15

g1 = vj.inv.ep.EpochG(file1)
g2 = vj.inv.ep.EpochG(file2)


y1 = g1.cumu_ts(site,'e',nth_subflt)
t1 = g1.get_epochs()

y2 = g2.cumu_ts(site,'e',nth_subflt)
t2 = g2.get_epochs()


from pylab import plt

plt.plot(t1, y1, 'x-',label='gravity')
plt.plot(t2, y2, 'o-',label='non-gravity')

plt.legend()
plt.show()
