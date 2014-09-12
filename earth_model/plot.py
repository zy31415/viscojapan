#!/usr/bin/env python3
from pylab import *

rad1=[]
vis=[]
elas_dep=60.
asth_dep=220.
upm_dep=670.
with open('earth.model') as fid:
    fid.readline()
    for ln in fid:
        tp=ln.split()
        rad1.append(float(tp[0]))
        if len(tp)==6:
            vis.append(float(tp[5]))
        elif len(tp)==8:
            vis.append(float(tp[7]))
        else:
            raise ValueError('Wrong file format.')
vis=asarray(vis)
rad1=asarray(rad1)
dep1=6371-rad1
vis*=1e18
semilogx(vis,dep1,label='Max Vis.')
grid('on')
title('Maxwellian Viscosity VS depth.')
plt.gca().invert_yaxis()
xlabel('viscosity')
ylabel('depth')
axhline(elas_dep,ls='--',color='red',label='Elas. Dep=%.1fkm'%elas_dep)
axhline(asth_dep,ls='--',color='green',label='Asth. Dep=%.1fkm'%asth_dep)
axhline(upm_dep,ls='--',color='blue',label='Upper Mantle =%.1fkm'%upm_dep)
axhline(2900,ls='--',color='black',label='Core-Mantle =%.1fkm'%2900)
legend(loc=4)
show()
