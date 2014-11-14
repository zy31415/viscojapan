#!/bin/bash
gmt psbasemap -U20/0/25/Yang -JB138/38/30/46/16c -K -P -B4 -R128/148/30/46 > out.ps
gmt grdimage ~tmp/grd -Q -O -K -C~tmp/cpt -J -R > out.ps
gmt pscoast -Swhite -R -O -K -J > out.ps
gmt psscale -Q -Baf::/:m: -K -C~tmp/cpt -D4/9/4/.2 -O > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -Sf0.25/3p -O -K -Wthick,150 -R -J -G150 > out.ps
gmt pscoast -Lf145/31/38/200+lkm+jt -Wfaint,100 -J -K -Na/faint,50,-- -Dh -R -O > out.ps
gmt psmeca /tmp/tmpib4sscf9 -O -Sc0.400000 -J -h1 -R > out.ps
