#!/usr/bin/env python

############################################################################
#
# This script produces the history plot graphics for the median number of
# Obama electoral votes as estimated on each day of the campgain season
# from April 1 to the present. It also includes the 95% confidence interval.
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
#    Oct  7, 2008 -- Highlight edge of 95% CI with green
#
############################################################################

import time 

import matplotlib
matplotlib.use('Agg')
from pylab import *

hfile = open("../matlab/EV_estimate_history.csv")
ev_hist = array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

# Build a numpy array from the CSV file, except for the last entry
for line in hfile:
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

dates = ev_hist[:,0]
medianBO = ev_hist[:,1]
modeBO = ev_hist[:,3]
lowBO95 = ev_hist[:,10]
highBO95 = ev_hist[:,11]

############################################################################
#
# Thumbnail-size graphic, 200px wide, for the right sidebar display
# throughout the blog.
#
############################################################################

subplot(111, axisbelow=True, axisbg='w')

plot((90, 320), (269, 269), '-r', linewidth=1)

xlim(92, 320)
ylim(157, 383)
yticks(arange(160, 400, 20))
xticks([92, 122, 153, 183, 214, 245, 275, 306],
		('          Apr','          May','          Jun',
		 '          Jul','          Aug','          Sep',
		 '          Oct','        Nov'), fontsize=19)


grid(color='#aaaaaa')

title("Median EV estimator", fontsize=27, fontweight='bold')
ylabel("Obama EV", fontsize=25, fontweight='bold')

plot(dates, medianBO, '-k', linewidth=2)

xs, ys = poly_between(dates, lowBO95, highBO95)
fill(xs, ys, '#222222', alpha=0.2, edgecolor='none')

show()
savefig(open('EV_history-200px.png', 'w'), dpi=25)

clf()

############################################################################
#
# Larger graphic, 500px wide, designed to fit in the center content column.
#
############################################################################

subplot(111, axisbelow=True, axisbg='w')

plot((90, 320), (269, 269), '-r', linewidth=1)

xlim(92, 320)
ylim(157, 383)
yticks(arange(160, 400, 20))
xticks([92,122,153,183,214,245,275,306],
		('            Apr','            May','            Jun',
		 '            Jul','            Aug','            Sep',
		 '            Oct','        Nov'), fontsize=16)


grid(color='#aaaaaa')

title("Median EV estimator with 95% confidence interval", fontsize=18,
		fontweight='bold')
ylabel("Obama EV",fontsize=16)
text(95, 172, time.strftime("%d-%b %I:%M%p %Z"), fontsize=14)
text(95, 159, "election.princeton.edu", fontsize=14)

plot(dates, medianBO, '-k', linewidth=2)

xs, ys = poly_between(dates, lowBO95, highBO95)
fill(xs, ys, '#222222', alpha=0.2, edgecolor='none')

plot(dates, highBO95, '-g', linewidth=1, alpha=0.5)
plot(dates, lowBO95, '-g', linewidth=1, alpha=0.5)

show()
savefig(open('EV_history-unlabeled.png', 'w'), dpi=62.5, facecolor='#fcfcf4',
		edgecolor='#fcfcf4')

## Annotations 
annotate("HRC withdraws", xy=(159, medianBO[67]), xytext=(159.01,
	medianBO[67]-42), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='center', verticalalignment='top', fontsize=12)
annotate("Celebrity ad", xy=(214, medianBO[122]+2), xytext=(214.01,
	medianBO[122]+44), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.08, width=0.5, headwidth=4),
	horizontalalignment='center', verticalalignment='top', fontsize=12)
annotate("McCain\nhouses\ngaffe", xy=(234, medianBO[142]), xytext=(234.01,
	medianBO[142]-41), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='center', verticalalignment='top', fontsize=12)
annotate("DNC", xy=(238, medianBO[146]-4), xytext=(238.01,
	medianBO[146]-20), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='left', verticalalignment='top', fontsize=12)
annotate("RNC", xy=(246, medianBO[154]+2), xytext=(246.01,
	medianBO[154]+43), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='left', verticalalignment='top', fontsize=12)
annotate("Palin on ABC\nMcCain on\n'The View'", xy=(256, medianBO[164]-4),
	xytext=(256.01, medianBO[164]-61), textcoords='data',
	arrowprops=dict(facecolor='darkblue', edgecolor='darkblue', shrink=0.075,
	width=0.5, headwidth=4), horizontalalignment='center',
	verticalalignment='top', fontsize=12)
annotate("Debate\n#1", xy=(270, medianBO[178]-6), xytext=(270.01,
	medianBO[178]-45), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='left', verticalalignment='top', fontsize=12)
annotate("#2", xy=(281, medianBO[189]-6), xytext=(281.01,
	medianBO[189]-60), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=0),
	horizontalalignment='left', verticalalignment='top', fontsize=12)
annotate("#3", xy=(289, medianBO[197]-14), xytext=(289.01,
	medianBO[197]-45), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=0),
	horizontalalignment='left', verticalalignment='top', fontsize=12)
## End Annotations 

show()
savefig(open('EV_history.png', 'w'), dpi=62.5, facecolor='#fcfcf4',
		edgecolor='#fcfcf4')

show()
savefig(open('EV_history-full_size.png', 'w'), facecolor='#fcfcf4',
		edgecolor='#fcfcf4')
