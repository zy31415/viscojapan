#!/bin/bash
gmt psbasemap -R95/160/12/55 -U18/25/0 -JB127.5/33.5/12/55/19c -K -B10g10 > out.ps
gmt grdimage ~topo.grd -K -J -O -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -I~topo_grad.grd > out.ps
gmt grdimage ~tmp/grd -R -K -Q -J -O -C~tmp/cpt > out.ps
gmt grdcontour ~tmp/grd -R -K -J -Wthick,red -A1+f8.000000+um -Gn1/.5c -O -C/tmp/tmpdmrqvtyb > out.ps
gmt psscale -K -C~tmp/cpt -D15.000000/8.000000/4/.2 -Q -O -Ba::/:m: > out.ps
gmt pscoast -R -K -A1000 -Lf155/15/35/500+lkm+jt -Na/faint,100,-. -Dl -Wfaint,50 -J -O > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -R -K -Sf0.25/3p -Wthick,100 -J -G100 -O > out.ps
gmt psmeca /tmp/tmpolhks1b5 -R -h1 -Sc0.200000 -J -O > out.ps
