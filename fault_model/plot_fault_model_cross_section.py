from pylab import plt

import viscojapan as vj

frame = vj.fm.FaultFramework(vj.fm.control_points3)

vj.fm.plot_fault_framework(frame)

plt.savefig('cross_section.pdf')
plt.show()
plt.close()
