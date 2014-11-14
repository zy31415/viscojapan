#!/bin/bash
gmt psbasemap -K -JB138/38/30/46/16c -B4 -R128/148/30/46 -U20/0/25/Yang -P > out.ps
gmt grdimage ~ver.grd -R -K -J -C~hor_mag.cpt -O > out.ps
gmt pscoast -R -K -Swhite -J -O > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -K -J -G150 -Sf0.25/3p -Wthick,150 -R -O > out.ps
gmt pscoast -Lf145/31/38/200+lkm+jt -K -J -Dh -Na/faint,50,-- -Wfaint,100 -R -O > out.ps
gmt grdcontour ~ver.grd -K -J -Gn1/.5c -C/tmp/tmpj445veo3 -R -A1+f8+um -O > out.ps
gmt psmeca /tmp/tmpk8cir96_ -K -h1 -J -R -Sc0.400000 -O > out.ps
gmt psscale -Q -Baf::/:m: -O -D4/9c/4c/.2c -Ccpt > out.ps
