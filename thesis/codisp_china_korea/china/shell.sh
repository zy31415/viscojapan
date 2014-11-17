#!/bin/bash
gmt psbasemap -B5 -JB117.5/37.5/20/55/15c -R95/140/20/55 -P -K -U20/0/22/Yang > out.ps
gmt grdimage ~topo.grd -I~topo_grad.grd -O -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -J -K > out.ps
gmt psvelo china_pred.in -A0.07i/0.1i/0.1i+a45+g+e -Gblack -Sr50/1/0 -J -W0.5,black -R -O -K -hi > out.ps
gmt psvelo /tmp/tmphl0oih32 -A0.07i/0.1i/0.1i+a45+g+e+jc -Gblack -Sr50.000000/1/0 -J -W0.5,black -R -O -K -hi > out.ps
gmt pstext /tmp/tmpcwdukd9z -R -O -K -J -F+f8+jLB > out.ps
gmt psvelo china_obs.in -A0.07i/0.1i/0.1i+a45+g+e -Gred -Sr50/1/0 -J -W0.5,red -R -O -K -hi > out.ps
gmt psvelo /tmp/tmp1f1c7ok5 -A0.07i/0.1i/0.1i+a45+g+e+jc -Gred -Sr50.000000/1/0 -J -W0.5,red -R -O -K -hi > out.ps
gmt pstext /tmp/tmp8klqc2a4 -R -O -K -J -F+f8+jLB > out.ps
gmt pscoast -A500 -Na/faint,50,-- -Dh -J -Wfaint,100 -R -O -K -Lf144/35.4/38/100+lkm+jt > out.ps
gmt psmeca /tmp/tmpcedy9wrj -J -R -O -Sc0.400000 -h1 > out.ps
