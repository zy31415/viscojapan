#!/bin/bash
gmt psbasemap -JB10/55/55/60/10c -K -R5/15/52/58 -B4g4>out.ps
gmt pscoast -J -R -Df -Wthinnest>out.ps
