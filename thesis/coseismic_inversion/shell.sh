#!/bin/bash
gmt psbasemap -U18/25/0 -B2 -K -R140/145/35/41.5 -P -JB142.5/38.5/35/41.5/14c > out.ps
gmt grdimage ~topo.grd -J -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -K -O -I~topo_grad.grd > out.ps
gmt grdimage ~mag.grd -C~mag.cpt -O -Q -R -I~topo_grad_resampled.grd -K -J -G > out.ps
gmt grdcontour ~mag.grd -C/tmp/tmp3peu7vmt -Wthick -O -A1+f9+um -R -K -J -Gn1/.5c > out.ps
gmt pscoast -K -Wfaint,50 -O -A1000 -Na/faint,100,-. -Lf155/15/35/500+lkm+jt -Dl -R -J > out.ps
gmt pslegend /tmp/tmph_1wnyie -K -C0.04i/0.07i -D143.5/35.2/4/1.2/BL -O -J -L1.2 -R -F+gazure1 > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -Wthick,red -O -J -Sf0.25/3p -K -R -Gred > out.ps
gmt psmeca /tmp/tmpdwgekejt -R -O -Sc0.400000 -h1 -J > out.ps
