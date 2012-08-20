#!/bin/sh

############################################################################
#
# This script postprocesses the resulting images which were produced by
# calling the pollcalc java program.
#
# Author: Andrew Ferguson <adferguson@alumni.princeton.edu>
#
# Script written for election.princeton.edu run by Samuel S.-H. Wang under
# noncommercial-use-only license:
# You may use or modify this software, but only for noncommericial purposes.
# To seek a commercial-use license, contact sswang@princeton.edu
#
# Update History:
#      Jul  8, 2012 -- Update for 2012 election
#
############################################################################

# Resize the yellow background one down for the Wordpress theme
convert -resize 500x500 -support 5.0 EV_map.png EV_map.png

# And cover over the text in the white one and shrink to fit in the sidebar
mv EV_map.png-white EV_map-white.png

convert -fill white -draw 'rectangle 0,354 345,419' \
	-fill white -draw 'rectangle 0,0 280,60' \
	-fill white -draw 'rectangle 442,275 550,500' \
	-resize 200x200 EV_map-white.png EV_map-200px.png

rm EV_map-white.png
