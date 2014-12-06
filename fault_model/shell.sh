#!/bin/bash
gmt psbasemap -U20/0/22/Yang -B2 -JB141.5/38.5/33.5/42/15c -P -K -R138/146/33.5/42 > out.ps
gmt grdimage ~topo.grd -O -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -J -K -I~topo_grad.grd > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/kur_top.in -O -Wthin,50 -J -K -R > out.ps
gmt psxy ../share/slab1.0/kur_contours_above_100km.in -O -SqL144/41.5/138/41.5:+Lh+ukm+f9,balck -Wthin,50,-- -J -K -R > out.ps
gmt pscoast -Dh -R -O -Wfaint,100 -J -Na/faint,50,-- -Lf145/34/38/100+lkm+jt -K > out.ps
gmt psxy /tmp/tmpkli9t2__ -O -Wthick,red -J -K -R > out.ps
gmt psxy /tmp/tmp10cw57_m -Gwhite -O -Ss0.400000 -J -Wthick,red -R -K > out.ps
gmt psxy /tmp/tmphpdpnwen -Gred -O -Sc0.050000 -J -Wthick,red -R -K > out.ps
gmt psmeca /tmp/tmpd1v2rh95 -J -R -O -T -Sm0.400000/8.000000 -h0 -Wblack -Lblack > out.ps
