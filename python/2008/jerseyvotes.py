#!/usr/bin/env python

############################################################################
#
# This script produces an HTML table which displays the relative influence
# voters in different swing states have over the outcome of the election.
# The influence statistic is normalized so that NJ voters, living in a
# non-swing state have power 1.0, hence the term "jerseyvotes." The statistic
# is calculated by the MATLAB script EV_jerseyvotes.m
#
# Author: Andrew Ferguson <adferguson@alumni.princeton.edu>
#
# Script written for election.princeton.edu run by Samuel S.-H. Wang under
# noncommercial-use-only license:
# You may use or modify this software, but only for noncommericial purposes.
# To seek a commercial-use license, contact sswang@princeton.edu
#
############################################################################

from decimal import Decimal

jerseyvotes = {}
statemargins = {}

# The jerseyvotes.csv file has the following format:
# index, state abbreviation, voter power (most powerful = 100)

jvfile = open("../matlab/jerseyvotes.csv")

for line in jvfile:
	values = line[:-1].split(",")
	jerseyvotes[values[1]] = Decimal(values[2])

jvfile.close()

# The stateprobs.csv file has the following format:
# prob. of Dem win, margin, prob. of Dem win with Dem 2% boost, prob. 
# 		of Dem win with Rep 2% boost, state abbreviation

spfile = open("../matlab/stateprobs.csv")

for line in spfile:
	values = line[:-1].split(",")
	statemargins[values[4]] = Decimal(values[1])

spfile.close()

# Output the HTML table displaying the jerseyvotes ranking. It will be
# included into the blog sidebar by a WordPress widget.

jvdisplay = open("jerseyvotes.html", "w")

jvdisplay.write('<table width="100%" style="text-align: center">\n')
jvdisplay.write("<tr>\n")
jvdisplay.write("\t<th>State</th><th>Margin</th><th>Power</th>\n")
jvdisplay.write("</tr>\n")

for state in sorted(jerseyvotes, key=lambda x: jerseyvotes[x], reverse=True):

	jvdisplay.write("<tr>\n")
	jvdisplay.write("\t<td>%s</td>" % state)

	margin = statemargins[state]
	
	if margin > 0:
		jvdisplay.write('<td style="color: blue">Obama +%s%%</td>' % margin)
	elif margin < 0:
		jvdisplay.write('<td style="color: red">McCain +%s%%</td>' % -margin)
	else:
		jvdisplay.write("<td>Tied</td>")
	
	if state != "NJ":
		jvdisplay.write("<td>%#.1f</td>\n" % jerseyvotes[state])
	else:
		jvdisplay.write("<td>%s</td>\n" % jerseyvotes[state]) # NJ power is not rounded
	jvdisplay.write("</tr>\n")

jvdisplay.write("</table>\n")
jvdisplay.close()
