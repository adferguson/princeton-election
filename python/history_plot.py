#!/usr/bin/env python

############################################################################
#
# This script produces the history plot graphics for the median number of
# Obama electoral votes as estimated on each day of the campgain season
# from May 22 to the present. It also includes the 95% confidence interval.
# These quantities are calculated by the MATLAB script EV_estimator.m. In
# stand-alone operation, the plot is drawn by the MATLAB script
# EV_history_plot.m, however we re-draw the plot here using Python's
# matplotlib for improved display on the web. (MATLAB also has a bug which
# causes it to crash when attempting to plot this graphic in an automated
# environment without a display.)
#
# Author: Andrew Ferguson <adferguson@alumni.princeton.edu>
#
# Script written for election.princeton.edu run by Samuel S.-H. Wang under
# noncommercial-use-only license:
# You may use or modify this software, but only for noncommericial purposes.
# To seek a commercial-use license, contact sswang@princeton.edu
#
# Update History:
#    Sep 10, 2012 -- Added some annotations
#    Sep  4, 2012 -- Relabel graph; lighten the band
#    Aug 12, 2012 -- Add support for comments in csv file; CI more translucent
#    Jul  8, 2012 -- Add year to large chart
#    Jul  7, 2012 -- Update for 2012
#    Oct  7, 2008 -- Highlight edge of 95% CI with green
#
############################################################################

import time 

import matplotlib
matplotlib.use('Agg')
from pylab import *

# May 22nd is day 143, April 1 is day 92
campaign_start = 143 # TODO(adf): calculate? also below in xticks

hfile = open("../matlab/EV_estimate_history.csv")
ev_hist = array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

# Build a numpy array from the CSV file, except for the last entry
for line in hfile:
    if line[0] != '#':
        ev_hist = append(ev_hist, [map(int, line[:-1].split(",")[:-1])], axis=0)

hfile.close()
ev_hist = delete(ev_hist, 0, 0)

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
#    1 value - metamargin

dates = ev_hist[:,0]
medianDem = ev_hist[:,1]
modeDem = ev_hist[:,3]
lowDem95 = ev_hist[:,10]
highDem95 = ev_hist[:,11]

############################################################################
#
# Thumbnail-size graphic, 200px wide, for the right sidebar display
# throughout the blog.
#
############################################################################

subplot(111, axisbelow=True, axisbg='w')

plot((campaign_start-2, 320), (269, 269), '-r', linewidth=1)

yticks(arange(160, 400, 20))
# TODO(adf): construct programatically (month starts after campaign_start)
xticks([campaign_start, 153, 183, 214, 245, 275, 306],
		('      May','          Jun',
		 '          Jul','          Aug','          Sep',
		 '          Oct','        Nov'), fontsize=19)


grid(color='#aaaaaa')

title("Median EV estimator", fontsize=27, fontweight='bold')
ylabel("Obama EV", fontsize=25, fontweight='bold')

plot(dates, medianDem, '-k', linewidth=2)

xs, ys = poly_between(dates, lowDem95, highDem95)
fill(xs, ys, '#222222', alpha=0.075, edgecolor='none')

xlim(campaign_start, 320)
ylim(157, 383)

show()
savefig(open('EV_history-200px.png', 'w'), dpi=25)

clf()

############################################################################
#
# Larger graphic, 500px wide, designed to fit in the center content column.
#
############################################################################

subplot(111, axisbelow=True, axisbg='w')

plot((campaign_start-2, 320), (269, 269), '-r', linewidth=1)

yticks(arange(160, 400, 20))
# TODO(adf): construct programatically (month starts after campaign_start)
xticks([campaign_start,153,183,214,245,275,306],
		('        May','            Jun',
		 '            Jul','            Aug','            Sep',
		 '            Oct','        Nov'), fontsize=16)


grid(color='#aaaaaa')

title("Median EV estimator", fontsize=18,
		fontweight='bold')
ylabel("Obama EV",fontsize=16)
text(campaign_start+3, 172, time.strftime("%d-%b-%Y %I:%M%p %Z"), fontsize=14)
text(campaign_start+3, 159, "election.princeton.edu", fontsize=14)

plot(dates, medianDem, '-k', linewidth=2)

xs, ys = poly_between(dates, lowDem95, highDem95)
fill(xs, ys, '#222222', alpha=0.075, edgecolor='none')

# hurricane tracker prediction
xs, ys = poly_between([308, 310], [262, 262], [357, 357])
fill(xs, ys, 'yellow', edgecolor='none')
xs, ys = poly_between([308, 310], [287, 287], [337, 337])
fill(xs, ys, 'red', edgecolor='none')
text(312, 327, "Prediction", fontsize=14, rotation='270')

xlim(campaign_start, 320)
ylim(157, 383)

show()
savefig(open('EV_history-unlabeled.png', 'w'), dpi=62.5, facecolor='#fcfcf4',
		edgecolor='#fcfcf4')

## Annotations 

# July 12
day=194
#annotate("Bain", xy=(day, medianDem[day-campaign_start]-2), xytext=(float(day) + 0.01,
annotate("Bain", xy=(day, 303), xytext=(float(day) + 0.01,
	303-42), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='center', verticalalignment='top', fontsize=12)
# August 11
day=224
#annotate("Ryan\nas VP", xy=(day, medianDem[day-campaign_start]+2), xytext=(float(day) + 0.01,
annotate("Ryan\nas VP", xy=(day, 333), xytext=(float(day) + 0.01,
	333+42), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='center', verticalalignment='top', fontsize=12)
# August 30
day=243
annotate("RNC", xy=(day, medianDem[day-campaign_start]+2), xytext=(float(day) + 0.01,
	medianDem[day-campaign_start]+42), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='center', verticalalignment='top', fontsize=12)
# Sept 6
day=250
annotate("DNC", xy=(day, medianDem[day-campaign_start]-2), xytext=(float(day) + 0.01,
	medianDem[day-campaign_start]-42), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='center', verticalalignment='top', fontsize=12)

## End Annotations 

show()
savefig(open('EV_history.png', 'w'), dpi=62.5, facecolor='#fcfcf4',
		edgecolor='#fcfcf4')

show()
savefig(open('EV_history-full_size.png', 'w'), facecolor='#fcfcf4',
		edgecolor='#fcfcf4')
