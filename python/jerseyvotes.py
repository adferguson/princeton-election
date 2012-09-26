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
# Update History:
#    Aug 19, 2012 -- moved to GitHub; future updates in commit messages
#    Jul  7, 2012 -- Initial port from 2008 version
#
############################################################################

from decimal import Decimal
from update_polls import state_names

huffpo_url_pattern = "http://elections.huffingtonpost.com/pollster/2012-%s-president-romney-vs-obama"

jerseyvotes = {}
statemargins = {}

def display_state(jvdisplay, state):
    jvdisplay.write("<tr>\n")
    jvdisplay.write("\t<td>%s</td>" % state)

    margin = statemargins[state]
    data_url = huffpo_url_pattern % state_names[state].lower().replace(" ", "-")
    
    if margin > 0:
        jvdisplay.write('<td><a href="%s" style="text-decoration: none; color: blue">'
                'Obama +%s%%</a></td>' % (data_url, margin))
    elif margin < 0:
        jvdisplay.write('<td><a href="%s" style="text-decoration: none; color: red">'
                'Romney +%s%%</a></td>' % (data_url, -margin))
    else:
        jvdisplay.write("<td>Tied</td>")
    
    if state != "NJ":
        jvdisplay.write("<td>%#.1f</td>\n" % jerseyvotes[state])
    else:
        jvdisplay.write("<td>%s</td>\n" % jerseyvotes[state]) # NJ power is not rounded
    jvdisplay.write("</tr>\n")

# The jerseyvotes.csv file has the following format:
# index, state abbreviation, voter power (most powerful = 100)

jvfile = open("../matlab/jerseyvotes.csv")

for line in jvfile:
    values = line[:-1].split(",")
    jerseyvotes[values[1]] = Decimal(values[2])

jvfile.close()

# The stateprobs.csv file has the following format:
# prob. of Dem win, margin, prob. of Dem win with Dem 2% boost, prob. 
#         of Dem win with Rep 2% boost, state abbreviation

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

top_states = sorted(jerseyvotes, key=lambda x: jerseyvotes[x], reverse=True)[:10]

for state in top_states:
    display_state(jvdisplay, state)

if "NJ" not in top_states:
    display_state(jvdisplay, "NJ")

jvdisplay.write("</table>\n")
jvdisplay.close()
