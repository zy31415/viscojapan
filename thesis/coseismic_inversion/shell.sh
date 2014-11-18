#!/bin/bash
gmt psbasemap -K -R140/145/35/41.5 -B2 -U18/25/0 -JB142.5/38.5/35/41.5/16c -P > out.ps
gmt grdimage ~topo.grd -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -K -J -I~topo_grad.grd -O > out.ps
gmt grdimage ~tmp/slip_cutted.grd -K -J -R -C~tmp/slip.cpt -G -I~tmp/intensity.grd -Q -O > out.ps
gmt grdcontour ~tmp/slip_cutted.grd -A1+f9+um -K -J -R -C/tmp/tmpso6vngg4 -Gn1/.5c -O -Wthickest > out.ps
gmt pslegend /tmp/tmpx8l16j91 -K -J -R -C0.04i/0.07i -L1.2 -O -D143.5/35.2/4/1.2/BL -F+gazure1 > out.ps
gmt pslegend /tmp/tmpqcfh4l7l -K -J -R -C0.04i/0.07i -L1.2 -O -D143.5/35.2/4/1.5/BL -F+gazure1 > out.ps
gmt pscoast -A1000 -K -J -Wfaint,50 -R -L144.3/36/38/50+lkm+jt -Na/faint,150,-. -O -Dh > out.ps
gmt psxy /tmp/tmpdd9ody2k -Ss0.4 -K -J -R -Gwhite -O -Wthick,red > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -K -J -R -Gred -O -Wthick,red -Sf0.25/3p > out.ps
gmt psmeca /tmp/tmprwohlfzd -J -h1 -R -O -Sc0.400000 > out.ps
