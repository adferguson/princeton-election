#!/usr/bin/env python

############################################################################
#
# This script produces the display at the top of the blog of the current
# median electoral votes for each candidate. It also generates the text for
# an email message which the cron daemon sends out.
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
#    Jul 7, 2012 -- Initial port from 2008 version
#
############################################################################

import time

def format_win_prob(prob):
    if prob >= 98.0:
        return "%.1f" % prob
    else:
        return "%.0f" % prob

## Estimated electoral votes and the current meta-margin

efile = open("../matlab/EV_estimates.csv")
values = efile.read()[:-1].split(",")
efile.close()

time_str = "%s %s, %s:%s" % (time.strftime("%B"), int(time.localtime()[2]),
		int(time.strftime("%I")), time.strftime("%M%p %Z"))

dem_ev = values[0]
gop_ev = values[1]
metamargin = float(values[12])

## Estimated win probabilities

efile = open("../matlab/EV_prediction_probs.csv")
values = efile.read()[:-1].split(",")
efile.close()

bayesian_win_prob = format_win_prob(float(values[0]) * 100.0)
drift_win_prob = format_win_prob(float(values[1]) * 100.0)

## Write the website header

evdisplay = open("current_ev.html", "w")

evdisplay.write('\t<li><a href="/history-of-electoral-votes-for-obama/">As of %s:</a></li>\n' % time_str)
evdisplay.write('\t<li><a href="/electoral-college-map/" style="color: blue">Obama: %s</a></li>\n' % dem_ev)
evdisplay.write('\t<li><a href="/electoral-college-map/" style="color: red">Romney: %s</a></li>\n' % gop_ev)

evdisplay.write('\t<li><a href="/faq/#metamargin">Meta-margin: ')

if metamargin > 0:
	evdisplay.write('Obama +%2.2f%%</a></li>\n' % metamargin)
elif metamargin < 0:
	evdisplay.write('Romney +%2.2f%%</a></li>\n' % -metamargin)
else:
	evdisplay.write('Tied</a></li>\n')

evdisplay.write('\t<li class="rss"><a href="http://election.princeton.edu/feed/">RSS</a></li>\n')
evdisplay.write('\t<li style="float: center; clear: both; padding-top: 0px;"><a href="http://election.princeton.edu/2012/10/27/landfall/">Probability of Obama re-election: Random Drift %s%%, Bayesian Prediction %s%%</a></li>\n' % (drift_win_prob, bayesian_win_prob))

evdisplay.close()

############################################################################

email_update = \
"""Today's update of the Meta-Analysis of State Polls at Princeton University
gives a median EV expectation of

Obama %s, Romney %s.

Obama's meta-margin is: %2.2f%%

This update is effective as of %s.

From
The Princeton Election Consortium
"""

email = open("email_update.txt", "w")
email.write(email_update % (dem_ev, gop_ev, metamargin, time_str))
email.close()
