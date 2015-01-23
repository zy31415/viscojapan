#!/bin/bash
gmt psbasemap -JD142.3716/38.2977/12/80/9i -R80/200/12/80 -B20 -K -U18/25/0 > out.ps
gmt grdimage /tmp/tmpreezvc19 -I/tmp/tmpjozl2d7n -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -O -K -J > out.ps
gmt grdcontour ~tmp/grd -R -C/tmp/tmpxzz71kz5 -Wthick,red -K -S100 -A1+f8.000000+um -J -O -GL142.37/38.30/80/60,142.37/38.30/90/20,142.37/38.30/-160/40,158/38.30/180/5 > out.ps
gmt pscoast -R -Na/faint,100,-. -Dh -K -A5000 -J -O -Lf190/15/35/1000+lkm+jt -Wfaint,50 > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -R -Wthick,100 -K -Sf0.25/3p+r+b -J -O -G100 > out.ps
gmt psmeca /tmp/tmp52ynwvw_ -R -T -Lblack -Wblack -K -Sm0.200000/0.000000 -J -O -h0 > out.ps
gmt psxy -R -J -O > out.ps
