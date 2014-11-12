#!/bin/bash
gmt psbasemap -B2 -JB142.5/38.5/35/41.5/14c -R140/145/35/41.5 -U18/25/0 -P -K > out.ps
gmt grdimage ~topo.grd -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -J -I~topo_grad.grd -K -O > out.ps
gmt grdimage ~mag.grd -C~mag.cpt -J -G -R -O -I~topo_grad_resampled.grd -K -Q > out.ps
gmt grdcontour ~mag.grd -C/tmp/tmps2iyddgq -J -Gn1/.5c -R -O -A1+f9+um -Wthick -K > out.ps
gmt pscoast -J -R -Dl -Wfaint,50 -Na/faint,100,-. -A1000 -O -K -Lf155/15/35/500+lkm+jt > out.ps
gmt pslegend /tmp/tmp4r4hcv2x -C0.04i/0.07i -J -F+gazure1 -D143.5/35.2/4/1.2/BL -R -O -L1.2 -K > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -J -Gred -R -O -Wthick,red -K -Sf0.25/3p > out.ps
gmt psmeca /tmp/tmpp92kxzt9 -J -R -O -h1 -Sc0.400000 > out.ps
