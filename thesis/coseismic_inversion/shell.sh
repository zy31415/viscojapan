#!/bin/bash
gmt psbasemap -B2 -P -JB142.5/38.5/35/41.5/14c -R140/145/35/41.5 -U18/25/0 -K > out.ps
gmt grdimage ~topo.grd -J -I~topo_grad.grd -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -O -K > out.ps
gmt grdimage ~tmp/slip_cutted.grd -J -Q -C~tmp/slip.cpt -O -I~tmp/intensity.grd -K -G -R > out.ps
gmt grdcontour ~tmp/slip_cutted.grd -J -Wthickest -C/tmp/tmpv58u0h7x -O -R -Gn1/.5c -A1+f9+um -K > out.ps
gmt pslegend /tmp/tmpxw3ngqph -J -L1.2 -C0.04i/0.07i -O -R -F+gazure1 -D143.5/35.2/4/1.2/BL -K > out.ps
gmt pslegend /tmp/tmpg22uvrkc -J -L1.2 -C0.04i/0.07i -O -R -F+gazure1 -D143.5/35.2/4/1.5/BL -K > out.ps
gmt pscoast -J -Dh -Na/faint,150,-. -O -R -L144.3/36/38/50+lkm+jt -Wfaint,50 -K -A1000 > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -J -Wthick,red -Sf0.25/3p -O -R -Gred -K > out.ps
gmt psmeca /tmp/tmpd6gh2pg0 -J -T -O -R -Sm0.400000/0.000000 -Lblack -h0 -Wblack > out.ps
