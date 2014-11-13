#!/bin/bash
gmt psbasemap -P -K -U18/25/0 -JB142.5/38.5/35/41.5/14c -R140/145/35/41.5 -B2 > out.ps
gmt grdimage ~topo.grd -I~topo_grad.grd -O -K -J -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt > out.ps
gmt grdimage ~tmp/slip_cutted.grd -O -I~tmp/intensity.grd -K -J -R -G -C~tmp/slip.cpt -Q > out.ps
gmt grdcontour ~tmp/slip_cutted.grd -O -A1+f9+um -J -Wthickest -R -Gn1/.5c -K -C/tmp/tmpoqw28baj > out.ps
gmt pslegend /tmp/tmp20cnqy_n -O -L1.2 -K -J -D143.5/35.2/4/1.2/BL -C0.04i/0.07i -R -F+gazure1 > out.ps
gmt pscoast -O -A1000 -Dh -J -Wfaint,50 -R -Na/faint,150,-. -Lf155/15/35/500+lkm+jt -K > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -O -K -J -Wthick,red -R -Gred -Sf0.25/3p > out.ps
gmt psmeca /tmp/tmpq1iz7xyj -O -h1 -J -R -Sc0.400000 > out.ps
