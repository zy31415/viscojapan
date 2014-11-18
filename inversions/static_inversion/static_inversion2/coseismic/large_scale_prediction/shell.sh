#!/bin/bash
gmt psbasemap -U18/25/0 -JD142.3716/38.2977/12/8/9i -K -R80/200/12/80 -B20 > out.ps
gmt pscoast -O -K -A5000 -R -Na/faint,100,-. -J -Dh -Lf155/15/35/500+lkm+jt -Wfaint,50 > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -O -K -R -G100 -J -Sf0.25/3p -Wthick,100 > out.ps
gmt psmeca /tmp/tmpmm8242wx -O -R -Sc0.200000 -J -h1 > out.ps
