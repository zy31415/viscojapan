#!/bin/bash
gmt psbasemap -K -JD142.3716/38.2977/12/80/9i -B20 -R80/200/12/80 -U18/25/0 > out.ps
gmt grdimage ~topo.grd -I~topo_grad.grd -J -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -K -O > out.ps
gmt grdcontour ~tmp/grd -Wthick,red -J -R -GL142.37/38.30/80/60,142.37/38.30/90/20,142.37/38.30/-160/40,158/38.30/180/5 -A1+f8.000000+um -C/tmp/tmpnqhd72so -K -O > out.ps
gmt pscoast -Dh -J -Lf190/15/35/1000+lkm+jt -R -Wfaint,50 -A5000 -O -K -Na/faint,100,-. > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -Sf0.25/3p -Wthick,100 -J -R -G100 -K -O > out.ps
gmt psmeca /tmp/tmphd5tijo1 -J -R -O -Sc0.200000 -h1 > out.ps
