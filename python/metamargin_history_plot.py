#!/usr/bin/env python

############################################################################
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
#    Aug 12, 2012 -- Add support for comments in csv file, and date to plot
#    Jul  8, 2012 -- Updated for 2012 election
#
############################################################################

import time 

import matplotlib
matplotlib.use('Agg')
from pylab import *
import datetime

def campaign_day(day):
    jan_one = datetime.date(datetime.date.today().year, 1, 1)
    return ((day - jan_one).days + 1)


campaign_start = campaign_day(datetime.date(2012, 5, 22))

hfile = open("../matlab/EV_estimate_history.csv")
ev_hist = array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
metamargin = array([[ 0 ]])

# Build a numpy array from the CSV file, except for the last entry
for line in hfile:
    if line[0] != '#':
        ev_hist = append(ev_hist, [map(int, line[:-1].split(",")[:-1])], axis=0)
        foo = line[:-1].split(",")[-1]
        metamargin = append(metamargin, [[ float(foo) ]], axis=0)

hfile.close()
ev_hist = delete(ev_hist, 0, 0)
metamargin = delete(metamargin, 0, 0)

#    Each line of EV_estimate_history should contain:
#    1 value - date code
#    2 values - medianEV for the two candidates, where a margin>0 favors the
#			first candidate (in our case, Obama);
#    2 values - modeEV for the two candidates;
#    3 values - assigned (>95% prob) EV for each candidate, with a third entry
#			for undecided;
#    4 values - confidence intervals for candidate 1's EV: +/-1 sigma, then
#			95% band; and
#    1 value - number of state polls used to make the estimates.
#	 1 value - metamargin

dates = ev_hist[:,0]
medianBO = ev_hist[:,1]
modeBO = ev_hist[:,3]
lowBO95 = ev_hist[:,10]
highBO95 = ev_hist[:,11]
metamargin = metamargin[:,0]

############################################################################
#
# Larger graphic, 500px wide, designed to fit in the center content column.
#
############################################################################

subplot(111, axisbelow=True, axisbg='w')

plot((90, 320), (0, 0), '-r', linewidth=1)

yticks(arange(-2, 10, 2))
# TODO(adf): construct programatically (month starts after campaign_start)
xticks([campaign_start,153,183,214,245,275,306],
		('        May','            Jun',
		 '            Jul','            Aug','            Sep',
		 '            Oct','        Nov'), fontsize=16)


grid(color='#aaaaaa')

title("History of the Meta-Margin, 2012", fontsize=18,
		fontweight='bold')
ylabel("Obama-Romney Popular Meta-Margin (%)",fontsize=16)
# y-coords for date label based on ylim below
text(campaign_start+3, -2.5, time.strftime("%d-%b-%Y %I:%M%p %Z"), fontsize=14)
text(campaign_start+3, -3.3, "election.princeton.edu", fontsize=14)

plot(dates, metamargin, '-k', linewidth=2)

#
# hurricane tracker prediction ... functions would be nice :-(
#
pfile = open("../matlab/EV_prediction_MM.csv")
prediction = {}

(prediction["1sigma_low"], prediction["1sigma_high"], prediction["2sigma_low"],
        prediction["2sigma_high"]) = map(float, pfile.read().strip().split(","))

pfile.close()

election = campaign_day(datetime.date(2012, 11, 6))

low = prediction["2sigma_low"]
high = prediction["2sigma_high"]
xs, ys = poly_between([dates[-1], election-2], [metamargin[-1], low], [metamargin[-1], high])
fill(xs, ys, 'yellow', alpha=0.3, edgecolor='none')
xs, ys = poly_between([election-2, election], [low, low], [high, high])
fill(xs, ys, 'yellow', edgecolor='none')

low = prediction["1sigma_low"]
high = prediction["1sigma_high"]
xs, ys = poly_between([dates[-1], election-2], [metamargin[-1], low], [metamargin[-1], high])
fill(xs, ys, 'red', alpha=0.2, edgecolor='red')
xs, ys = poly_between([election-2, election], [low, low], [high, high])
fill(xs, ys, 'red', edgecolor='none')
#
# end hurricane tracker prediction
#

## Election Day indicator
axvline(x=election, linestyle='--', color='black')

xlim(campaign_start, 320)
ylim(-3.5, 9.5)

show()
savefig(open('MM_history-unlabeled.png', 'w'), dpi=62.5, facecolor='#fcfcf4',
		edgecolor='#fcfcf4')
