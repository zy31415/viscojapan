#!/bin/bash
gmt psbasemap -K -R80/200/12/80 -U20/25/0 -JD142.3716/38.2977/12/80/9i -B20 > out.ps
gmt grdimage ~topo.grd -K -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -J -I~topo_grad.grd -O > out.ps
gmt grdcontour ~tmp/grd -Wthick,red -A1+f8.000000+um -J -K -GL142.37/38.30/80/60,142.37/38.30/90/20,142.37/38.30/-160/40,158/38.30/180/5 -C/tmp/tmpkmtny6__ -O -R > out.ps
gmt pscoast -Wfaint,50 -Na/faint,100,-. -A5000 -J -Dh -K -Lf190/20/35/1000+lkm+jt -O -R > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -Wthick,100 -J -K -Sf0.25/3p -G100 -O -R > out.ps
gmt psmeca /tmp/tmpr0hwqwzj -h1 -J -Sc0.200000 -O -R > out.ps
