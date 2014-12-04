#!/bin/bash
gmt psbasemap -B20 -R80/200/12/80 -JD142.3716/38.2977/12/80/9i -K -U18/25/0 > out.ps
gmt grdimage ~topo.grd -J -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -O -K -I~topo_grad.grd > out.ps
gmt grdcontour ~tmp/grd -C/tmp/tmpgwhz99gu -O -A1+f8.000000+um -K -J -R -S100 -Wthick,red -GL142.37/38.30/80/60,142.37/38.30/90/20,142.37/38.30/-160/40,158/38.30/180/5 > out.ps
gmt pscoast -O -A5000 -K -Na/faint,100,-. -J -R -Wfaint,50 -Lf190/15/35/1000+lkm+jt -Dh > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -O -K -Sf0.25/3p -J -R -Wthick,100 -G100 > out.ps
gmt psmeca /tmp/tmpswf3167d -O -J -h0 -Lblack -T -R -Sm0.200000/0.000000 -Wblack > out.ps
