#!/bin/bash
gmt psbasemap -R80/200/12/80 -U18/25/0 -JD142.3716/38.2977/12/80/9i -B20 -K > out.ps
gmt grdimage ~topo.grd -O -J -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -K -I~topo_grad.grd > out.ps
gmt grdcontour ~tmp/grd -A1+f8.000000+um -S100 -J -GL142.37/38.30/80/60,142.37/38.30/90/20,142.37/38.30/-160/40,158/38.30/180/5 -Wthick,red -R -O -C/tmp/tmpbqb5md97 -K > out.ps
gmt pscoast -A5000 -Wfaint,50 -J -K -R -O -Dh -Na/faint,100,-. -Lf190/15/35/1000+lkm+jt > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -Wthick,100 -Sf0.25/3p+r+b -J -K -R -O -G100 > out.ps
gmt psmeca /tmp/tmp4bpsjt1c -Sm0.200000/0.000000 -Wblack -Lblack -J -O -T -h0 -R > out.ps
