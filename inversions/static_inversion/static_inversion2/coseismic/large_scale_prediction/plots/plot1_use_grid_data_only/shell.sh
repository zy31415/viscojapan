#!/bin/bash
gmt psbasemap -U18/25/0 -JD142.3716/38.2977/12/80/9i -K -B20 -R80/200/12/80 > out.ps
gmt grdimage ~topo.grd -I~topo_grad.grd -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -J -K -O > out.ps
gmt grdcontour ~tmp/grd -GL142.37/38.30/80/60,142.37/38.30/90/20,142.37/38.30/-160/40,158/38.30/180/5 -Wthick,red -J -R -C/tmp/tmphodaz82_ -O -K -A1+f8.000000+um -S4 > out.ps
gmt pscoast -Wfaint,50 -Na/faint,100,-. -R -Dh -J -K -Lf190/15/35/1000+lkm+jt -A5000 -O > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -G100 -Wthick,100 -R -Sf0.25/3p -J -K -O > out.ps
gmt psmeca /tmp/tmprwqvwb0u -T -Lblack -O -Wblack -R -J -h0 -Sm0.200000/0.000000 > out.ps
