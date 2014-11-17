#!/bin/bash
gmt psbasemap -R95/160/12/55 -B10g10 -K -JB127.5/33.5/12/55/19c -U18/25/0 > out.ps
gmt grdimage ~topo.grd -I~topo_grad.grd -J -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -K -O > out.ps
gmt grdimage ~tmp/grd -Q -C~tmp/cpt -K -O -R -J > out.ps
gmt grdcontour ~tmp/grd -C/tmp/tmp_xk_9v3t -K -A1+f8.000000+um -R -J -Gn1/.5c -O -Wthick,red > out.ps
gmt psscale -Q -C~tmp/cpt -K -D15.000000/8.000000/4/.2 -O -Ba::/:m: > out.ps
gmt pscoast -Na/faint,100,-. -K -Dl -R -Lf155/15/35/500+lkm+jt -A1000 -J -O -Wfaint,50 > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -G100 -K -Sf0.25/3p -O -R -J -Wthick,100 > out.ps
gmt psmeca /tmp/tmpizolrp9c -h1 -Sc0.200000 -O -R -J > out.ps
