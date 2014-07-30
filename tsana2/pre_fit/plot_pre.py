from viscojapan.tsana.pre_fit.plot_pre_fit import plot_pre, plt

site = 'CNMR'
cmpt = 'e'

plot_pre('linres/%s.%s.lres'%(site,cmpt))
plt.legend()
plt.show()

