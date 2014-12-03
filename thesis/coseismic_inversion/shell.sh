#!/bin/bash
gmt psbasemap -R140/145/35/41.5 -P -B2 -U18/25/0 -K -JB142.5/38.5/35/41.5/14c > out.ps
gmt grdimage ~topo.grd -I~topo_grad.grd -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -J -K -O > out.ps
gmt grdimage ~tmp/slip_cutted.grd -R -I~tmp/intensity.grd -Q -J -C~tmp/slip.cpt -O -K -G > out.ps
gmt grdcontour ~tmp/slip_cutted.grd -R -Wthickest -J -A1+f9+um -C/tmp/tmp_gxxwhn5 -O -K -Gn1/.5c > out.ps
gmt pslegend /tmp/tmpfgo186q3 -R -F+gazure1 -D143.5/35.2/4/1.2/BL -J -L1.2 -C0.04i/0.07i -O -K > out.ps
gmt pslegend /tmp/tmpwzlaskeo -R -F+gazure1 -D143.5/35.2/4/1.5/BL -J -L1.2 -C0.04i/0.07i -O -K > out.ps
gmt pscoast -R -Na/faint,150,-. -Dh -J -A1000 -L144.3/36/38/50+lkm+jt -O -Wfaint,50 -K > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -R -Wthick,red -J -Sf0.25/3p -O -K -Gred > out.ps
gmt psmeca /tmp/tmpjy90gfum -R -Sm0.400000 -J -h0 -T -O > out.ps
