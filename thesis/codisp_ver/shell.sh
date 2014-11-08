#!/bin/bash
gmt psbasemap -B4:.Magnitude of the Oberseved Vertical Coseismic Disp: -R128/148/30/46 -P -U20/0/25/Yang -JB138/38/30/46/16c -K > out.ps
gmt grdimage ~ver_mag.grd -C~hor_mag.cpt -K -Q -O -J -R > out.ps
gmt pscoast -O -Swhite -J -K -R > out.ps
gmt psxy /home/zy/workspace/viscojapan/share/plate_boundary_PB/PB2002_boundaries.gmt -G150 -K -Wthick,150 -O -Sf0.25/3p -J -R > out.ps
gmt pscoast -Dh -R -Wfaint,100 -O -Lf145/31/38/200+lkm+jt -J -Na/faint,50,-- -K > out.ps
gmt grdcontour ~ver.grd -C/tmp/tmp2gre6fjf -R -O -A1+f9+um -Gn1/.5c -J -K > out.ps
gmt psmeca /tmp/tmpq8ipc8aa -h1 -K -O -Sc0.4 -J -R > out.ps
gmt psscale -Baf::/:m: -O -C~hor_mag.cpt -D4/9c/4c/.2c -Q > out.ps
