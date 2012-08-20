#!/usr/bin/env python

############################################################################
#
#
# Author: Andrew Ferguson <adferguson@alumni.princeton.edu>
#
# Script written for election.princeton.edu run by Samuel S.-H. Wang under
# noncommercial-use-only license:
# You may use or modify this software, but only for noncommericial purposes.
# To seek a commercial-use license, contact sswang@princeton.edu
#
############################################################################

import time

efile = open("../matlab/Sen_estimates.csv")
values = efile.read()[:-1].split(",")
efile.close()

dem_mode = values[0]
gop_mode = values[1]
probDem60 = float(values[2])

sendisplay = open("senate_current.html", "w")

sendisplay.write('\t<b>Dem Mode:</b> %s seats<br />\n' % dem_mode)
sendisplay.write('\t<b>GOP Mode:</b> %s seats<br />\n' % gop_mode)
sendisplay.write('\t<b>Chance of >= 60 seats:</b> %.1f%%<br />'
		'\n' % probDem60)

sendisplay.close()
