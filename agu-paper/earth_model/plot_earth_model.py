from pylab import plt
import matplotlib.gridspec as gridspec

import viscojapan as vj


reader = vj.em.EarthModelFileReader('./earth.modelBURG-SUM_51km')

dep = -reader.dep_top
den = reader.density
shear = reader.shear/10**9
bulk = reader.bulk/10**9
vis = reader.visM

def double_x(x):
    out = []
    for x1, x2 in zip(x[0:], x[1:]):
        out += [x1, x2]
    return out

def double_y(y):
    out = []
    for yi in y[:-1]:        
        out += [yi, yi]
    return out

dep = double_x(dep)
den = double_y(den)
shear = double_y(shear)
bulk = double_y(bulk)

## begin to plot

def axhspan_for_viscosity(ax):
    deps = [0,-51,-220,-670,-2000]
    cols = ['.95', '0.83', '0.7', '0.5']
    alpha = .8
    for dep1, dep2, col in zip(deps[0:], deps[1:], cols):
        ax.axhspan(dep2, dep1, color=col, alpha=alpha)

gs = gridspec.GridSpec(1, 3,
                       width_ratios=[1.5,1.7,1.1]
                       )

fig = plt.gcf()
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1], sharey=ax1)
ax3 = plt.subplot(gs[2], sharey=ax1)


# plot ax1 - Maxwell viscosity
axhspan_for_viscosity(ax1)
ax1.tick_params(axis='x', bottom='off', top='off', labelbottom='off')

ax1.text(0.2, -40,
         s='crust  $H_e=?$',
         fontsize=12)
ax1.text(0.2, -170,
         s='asthenosphere \n$ \\eta = ?$',
         fontsize=12)
ax1.text(0.2, -450,
         s='uppermantle \n$ \\eta = 1 \\times 10^{20}$',
         fontsize=12)
ax1.text(0.2, -850,
         s='lowermantle \n$ \\eta = 1 \\times 10^{21}$',
         fontsize=12)
ax1.set_ylabel('depth (km)')

# plot ax2 - shear and bulk modulus
axhspan_for_viscosity(ax2)
plt.setp(ax2.get_yticklabels(), visible=False)
ax2.plot(shear, dep, '--', label='shear modulus',
         dashes=(3,3),
         lw=2)
ax2.plot(bulk, dep, label='bulk modulus',
         lw=2)
plt.setp(ax2.get_xticklabels(), rotation=90)
ax2.set_xlabel('Shear/bulk modulus (GPa)')
ax2.legend(prop={'size':8})
ax2.set_xlim([0, 460])
    
# plot ax3 - density
axhspan_for_viscosity(ax3)
plt.setp(ax3.get_yticklabels(), visible=False)
ax3.plot(den, dep, lw=2)
ax3.set_xlim([2.2, 5])
plt.setp(ax3.get_xticklabels(), rotation=90)
ax3.set_xlabel(r'Density $(g/cm^3)$')

fig.subplots_adjust(wspace=.05)
plt.ylim([-1000,0])
plt.savefig('earth_model.pdf')
plt.savefig('earth_model.png')
plt.show()
