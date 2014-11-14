#!/bin/bash
gmt psbasemap -K -B4 -JB138/38/30/46/16c -P -R128/148/30/46 -U20/0/25/Yang > out.ps
gmt grdimage ~grd -Q -C~cpt -K -R -O -J > out.ps
gmt pscoast -Swhite -R -O -J -K > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -Wthick,150 -J -K -R -O -Sf0.25/3p -G150 > out.ps
gmt pscoast -Wfaint,100 -Na/faint,50,-- -Dh -K -J -Lf145/31/38/200+lkm+jt -R -O > out.ps
gmt psmeca /tmp/tmpimog1nyx -Sc0.400000 -J -K -R -O -h1 > out.ps
gmt psscale -O -Baf::/:m: -Q -D4/9c/4c/.2c -C~cpt > out.ps
