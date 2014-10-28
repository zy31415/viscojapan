#!/usr/bin/env python3
from pylab import *
L=4000.
rE=6371.
alpha=L/rE

theta=linspace(pi/2-0.3*alpha,pi/2+0.7*alpha,500)

# earth surface
x=rE*cos(theta)
y=rE*sin(theta)
plot(x,y)

# elastic lithosphere
rL=rE-60.
x=rL*cos(theta)
y=rL*sin(theta)
plot(x,y)
annotate('Elastic Lithosphere', (-555,6283.17), (-1200, 6500),
         arrowprops=dict(arrowstyle="->"),
         fontsize = 12)

# asthenosphere
rA=rE-220.
x=rA*cos(theta)
y=rA*sin(theta)
plot(x,y)
text(-220, 6200, 'Asthenosphere', fontsize=9)

# upper mantle
rA=rE-670.
x=rA*cos(theta)
y=rA*sin(theta)
plot(x,y)
text(-350, 5850,'Upper Mantle')

# core-mantle
rA=rE-2900.
x=rA*cos(theta)
y=rA*sin(theta)
plot(x,y)
text(100, 4500,'Mantle')
text(100, 3200,'Core')

# mark epicentor:
theta=pi/2
x=rE*cos(theta)
y=rE*sin(theta)
plot(x,y,marker='s',ms=8,label='Epicenter',ls='')

# mark J550:
from pyproj import Geod
g=Geod(ellps='WGS84')
ep=142.3765, 38.2966
site_pos=141.5020, 38.3011
tp=g.inv(site_pos[0],site_pos[1],ep[0],ep[1])
dis=tp[2]
theta=pi/2+dis/1e3/rE
x=rE*cos(theta)
y=rE*sin(theta)
plot(x,y,marker='^',ms=8,label='J550',ls='')

# mark J465:
from pyproj import Geod
g=Geod(ellps='WGS84')
ep=130.7649, 32.8421
site_pos=141.5020, 38.3011
tp=g.inv(site_pos[0],site_pos[1],ep[0],ep[1])
dis=tp[2]
theta=pi/2+dis/1e3/rE
x=rE*cos(theta)
y=rE*sin(theta)
plot(x,y,marker='^',ms=8,label='J465, Kyushu',ls='')

# mark ULAB:
from pyproj import Geod
g=Geod(ellps='WGS84')
ep=130.7649, 32.8421
site_pos=107.0523, 47.8652
tp=g.inv(site_pos[0],site_pos[1],ep[0],ep[1])
dis=tp[2]
theta=pi/2+dis/1e3/rE
x=rE*cos(theta)
y=rE*sin(theta)
plot(x,y,marker='^',ms=8,label='ULAB, 3034km',ls='')

axis('equal')
axvline(0.,ls='--',color='gray')
legend(loc=3,numpoints=1, prop={'size':10})
ylim([3000, 7000])

savefig('spherical_effec.pdf')
show()
