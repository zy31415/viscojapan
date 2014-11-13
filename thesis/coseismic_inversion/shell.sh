#!/bin/bash
gmt psbasemap -B2 -JB142.5/38.5/35/41.5/14c -U18/25/0 -P -K -R140/145/35/41.5 > out.ps
gmt grdimage ~topo.grd -I~topo_grad.grd -J -O -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -K > out.ps
gmt grdimage ~tmp/slip_cutted.grd -I~tmp/intensity.grd -J -O -G -K -Q -R -C~tmp/slip.cpt > out.ps
gmt grdcontour ~tmp/slip_cutted.grd -J -A1+f9+um -O -Wthickest -Gn1/.5c -K -R -C/tmp/tmpq2p4w1_u > out.ps
gmt pslegend /tmp/tmpm04e380i -J -O -K -F+gazure1 -R -C0.04i/0.07i -D143.5/35.2/4/1.2/BL -L1.2 > out.ps
gmt pslegend /tmp/tmpq4fligra -J -O -K -F+gazure1 -R -C0.04i/0.07i -D143.5/35.2/4/1.5/BL -L1.2 > out.ps
gmt pscoast -J -A1000 -O -Wfaint,50 -K -R -Na/faint,150,-. -Dh -L144.3/36/38/50+lkm+jt > out.ps
gmt psxy /tmp/tmpxhun91vs -J -O -Wthick,red -Gwhite -K -R -Ss0.4 > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -J -O -Wthick,red -Gred -K -Sf0.25/3p -R > out.ps
gmt psmeca /tmp/tmp3o6uw9fh -h1 -J -O -R -Sc0.400000 > out.ps
