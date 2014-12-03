#!/bin/bash
gmt psbasemap -JB141.5/38.5/33.5/42/15c -K -B2 -R138/146/33.5/42 -P -U20/0/22/Yang > out.ps
gmt grdimage ~topo.grd -J -I~topo_grad.grd -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -K -O > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/kur_top.in -J -R -K -Wthin,50 -O > out.ps
gmt psxy ../share/slab1.0/kur_contours_above_100km.in -J -K -R -Wthin,50,-- -SqL144/41.5/138/41.5:+Lh+ukm -O > out.ps
gmt pscoast -J -Lf145/34/38/100+lkm+jt -R -Dh -K -Na/faint,50,-- -Wfaint,100 -O > out.ps
gmt psxy /tmp/tmp0q9klygi -J -R -K -Wthick,red -O > out.ps
gmt psxy /tmp/tmpzv4fnk7n -J -Ss0.400000 -K -Gwhite -R -Wthick,red -O > out.ps
gmt psxy /tmp/tmpb9amyo3g -J -Sc0.050000 -K -Gred -R -Wthick,red -O > out.ps
gmt psmeca /tmp/tmppdy4cb82 -J -Sc0.400000 -R -h1 -O > out.ps
