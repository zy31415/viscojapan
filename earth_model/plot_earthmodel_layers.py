#!/usr/bin/env python3
from pylab import *
from matplotlib.path import Path
import matplotlib.patches as patches

ax=gca()
ax.invert_yaxis()

plot([0,700,700,0,0],[0,0, 670,670,0],'k',lw=4)

####
# Elastic layer
ax.text(100,20,r'Elastic Upper Crust ($0 \sim H_{e} km$)',
        verticalalignment='top',
        fontsize=12)

########
# plot soft layer
verts = [
    (0., 63.), # left, bottom
    (700., 63.), # left, top
    (700., 220.), # right, top
    (0., 220.), # right, bottom
    (0., 0.), # ignored
    ]

codes = [Path.MOVETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.CLOSEPOLY,
         ]

path = Path(verts, codes)
patch = patches.PathPatch(path, facecolor='lightgreen', lw=2)
ax.add_patch(patch)
ax.text(100,90,r'''Maxwell Viscoelastic Lower Crust ($H_e \sim 220km$)
$\eta_s (Pa \cdot s)$
''',
        verticalalignment='top')
#plot([0,700,700,0,0],[63,63,220,220,63])

########
# Upper Mantle
ax.text(100,400,r'''Maxwell Viscoelastic Upper Mantle (220~670km)
$\eta=1.0 \times 10^{20} Pa \cdot s$
''',
        verticalalignment='top')

########
# Lower Mantle
ax.text(100,700,r'''Maxwell Viscoelastic Lower Mantle (670~2891km)
$\eta=1.0 \times 10^{21} Pa \cdot s$
''',
        verticalalignment='top')

#########
# Overall labels
ID='Earth Model'
title('Earth Model')
ylabel('Dep(km)')
xlabel('(km)')
ylim((880,-100))
#axis('equal')
savefig('earthmodel_layer.png')
savefig('earthmodel_layer.pdf')
show()
