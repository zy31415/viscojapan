#!/bin/bash
gmt psbasemap -JB140/38/28/48/18c -B4g4 -K -U18/25/0 -R128/150/30/46 > out.ps
gmt grdimage topo.grd -O -C../../share/topo/ETOPO1.cpt -J -K -Itopo_grad.grd > out.ps
gmt pscoast -Wfaint,30 -O -A1000 -J -K -Lf146/32/38/200+lkm+jt -R -Dl -Na/faint,50,-- > out.ps
gmt psxy share/plate_boundary_PB/PB2002_boundaries.gmt -O -Wthick,red -K -R -J -Sf0.25/3p -Gred > out.ps
gmt psxy /tmp/tmpc6u5otno -O -W5, red -SV0.15i/0.15i/0.4i+a100+g+e -R -J -Gred -K > out.ps
gmt pstext /tmp/tmp5u25s6ec -O -J -K -R -F+a0+f10,Helvetica,red+jCM > out.ps
gmt pstext /tmp/tmpn11_vqub -O -J -K -R -F+a70+f10,Helvetica-Bold,black+jCM > out.ps
gmt pstext /tmp/tmp568dcppq -O -J -K -R -F+a0+f12,Helvetica-Bold,yellow+jCM > out.ps
gmt psmeca /tmp/tmpgwvteq2x -O -Sc0.4 -h1 -R -J -K > out.ps
gmt psscale -O -D10/-1/6/.4h -Baf -C../../share/topo/ETOPO1.cpt > out.ps
