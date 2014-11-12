#!/bin/bash
gmt psbasemap -R95/160/12/55 -U18/25/0 -B10g10 -JB127.5/33.5/12/55/19c -K > out.ps
gmt grdimage ~topo.grd -J -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -O -K -I~topo_grad.grd > out.ps
gmt grdimage ~hor_mag_masked.grd -R -J -G -Q -K -C~hor_mag.cpt -O > out.ps
gmt pscoast -Na/faint,100,-. -R -J -K -O -Dl -Wfaint,50 -Lf155/15/35/500+lkm+jt -A1000 > out.ps
gmt psscale -D0.3/12.5/4c/.2c -Q -K -C~hor_mag.cpt -O -Baf::/:m: > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -R -J -G100 -Sf0.25/3p -K -O -Wthick,100 > out.ps
gmt psmeca /tmp/tmp3v4v4v3f -R -J -h1 -Sc0.200000 -O > out.ps
