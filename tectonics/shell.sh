#!/bin/bash
gmt psbasemap -JB140/38/28/48/18c -B4g4 -R128/150/30/46 -U -K > out.ps
gmt grdimage topo.grd -J -K -C../share/topo/ETOPO1.cpt -O -Itopo_grad.grd > out.ps
gmt pscoast -Na/faint,50,-- -Dl -R -O -Wfaint,30 -K -J -A1000 -Lf146/32/38/200+lkm+jt > out.ps
gmt psxy share/plate_boundary_PB/PB2002_boundaries.gmt -J -K -R -O -Wthick,red > out.ps
gmt psxy /tmp/tmpo5a6rdn6 -K -R -O -W5, red -SV0.15i/0.15i/0.4i+a100+g+e -J -Gred > out.ps
gmt pstext /tmp/tmpq0p3118e -J -K -R -O -F+a0+f10,Helvetica,red+jCM > out.ps
gmt pstext /tmp/tmp_j53um1p -J -K -R -O -F+a70+f10,Helvetica-Bold,black+jCM > out.ps
gmt pstext /tmp/tmpjcnp9zdo -J -K -R -O -F+a0+f12,Helvetica-Bold,yellow+jCM > out.ps
gmt psmeca /tmp/tmpth3l1bx1 -K -R -O -Sc0.4 -J -h1 > out.ps
gmt psscale -D10/-1/6/.4h -C../share/topo/ETOPO1.cpt -O -Baf > out.ps
