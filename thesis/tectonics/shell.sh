#!/bin/bash
gmt psbasemap -U18/25/0 -R128/150/30/46 -JB140/38/28/48/18c -K -B4g4 > out.ps
gmt grdimage topo.grd -J -O -K -C../../share/topo/ETOPO1.cpt -Itopo_grad.grd > out.ps
gmt pscoast -A1000 -R -O -K -Dl -J -Wfaint,30 -Lf146/32/38/200+lkm+jt -Na/faint,50,-- > out.ps
gmt psxy share/plate_boundary_PB/PB2002_boundaries.gmt -R -J -O -K -Gred -Sf0.25/3p -Wthick,red > out.ps
gmt psxy /tmp/tmp0o4dis69 -R -O -K -SV0.15i/0.15i/0.4i+a100+g+e -J -Gred -W5, red > out.ps
gmt pstext /tmp/tmpt6qj4lj2 -R -O -F+a0+f10,Helvetica,red+jCM -J -K > out.ps
gmt pstext /tmp/tmp_8b39o2h -R -O -F+a70+f10,Helvetica-Bold,black+jCM -J -K > out.ps
gmt pstext /tmp/tmpplb1vzxv -R -O -F+a0+f12,Helvetica-Bold,yellow+jCM -J -K > out.ps
gmt psmeca /tmp/tmp0q7cljbr -R -O -K -Sc0.4 -J -h1 > out.ps
gmt psscale -D10/-1/6/.4h -O -Baf -C../../share/topo/ETOPO1.cpt > out.ps
