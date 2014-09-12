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

# asthenosphere
rA=rE-220.
x=rA*cos(theta)
y=rA*sin(theta)
plot(x,y)

# upper mantle
rA=rE-670.
x=rA*cos(theta)
y=rA*sin(theta)
plot(x,y)

# core-mantle
rA=rE-2900.
x=rA*cos(theta)
y=rA*sin(theta)
plot(x,y)

# mark epicentor:
theta=pi/2
x=rE*cos(theta)
y=rE*sin(theta)
plot(x,y,marker='s',ms=8,label='Epi',ls='')

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
plot(x,y,marker='^',ms=8,label='ULAB',ls='')

axis('equal')
axvline(0.,ls='--',color='gray')
legend(loc=3,numpoints=1)
show()
