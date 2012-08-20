#!/usr/bin/env python

############################################################################
#
# This script produces the history plot graphics for the median number of
# McCain electoral votes as estimated on each day of the campgain season
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
medianJM = 538 - ev_hist[:,1]
modeJM = 538 - ev_hist[:,3]
highJM95 = 538 - ev_hist[:,10]
lowJM95 = 538 - ev_hist[:,11]

############################################################################
#
# Thumbnail-size graphic, 200px wide, for the right sidebar display
# throughout the blog.
#
############################################################################

subplot(111, axisbelow=True, axisbg='w')

plot((90, 320), (269, 269), '-r', linewidth=1)

xlim(92, 320)
ylim(137, 363)
yticks(arange(140, 380, 20))
xticks([92, 122, 153, 183, 214, 245, 275, 306],
		('          Apr','          May','          Jun',
		 '          Jul','          Aug','          Sep',
		 '          Oct','        Nov'), fontsize=19)


grid(color='#aaaaaa')

title("Median EV estimator", fontsize=27, fontweight='bold')
ylabel("McCain EV", fontsize=25, fontweight='bold')
text(95, 142, time.strftime("%d-%b %I:%M%p %Z"), fontsize=21)

plot(dates, medianJM, '-k', linewidth=2)

xs, ys = poly_between(dates, lowJM95, highJM95)
fill(xs, ys, '#222222', alpha=0.2, edgecolor='none')

show()
savefig(open('McCain-EV_history-200px.png', 'w'), dpi=25)

clf()

############################################################################
#
# Larger graphic, 500px wide, designed to fit in the center content column.
#
############################################################################

subplot(111, axisbelow=True, axisbg='w')

plot((90, 320), (269, 269), '-r', linewidth=1)

xlim(92, 320)
ylim(137, 363)
yticks(arange(140, 380, 20))
xticks([92,122,153,183,214,245,275,306],
		('            Apr','            May','            Jun',
		 '            Jul','            Aug','            Sep',
		 '            Oct','        Nov'), fontsize=16)


grid(color='#aaaaaa')

title("Median EV estimator with 95% confidence interval", fontsize=18,
		fontweight='bold')
ylabel("McCain EV",fontsize=16)
text(95, 150, time.strftime("%d-%b %I:%M%p %Z"), fontsize=14)
text(95, 137, "election.princeton.edu", fontsize=14)

plot(dates, medianJM, '-k', linewidth=2)

xs, ys = poly_between(dates, lowJM95, highJM95)
fill(xs, ys, '#222222', alpha=0.2, edgecolor='none')

show()
savefig(open('McCain-EV_history-unlabeled.png', 'w'), dpi=62.5,
		facecolor='#fcfcf4', edgecolor='#fcfcf4')

## Annotations 
annotate("HRC withdraws", xy=(159, medianJM[67]), xytext=(159.01,
	medianJM[67]+40), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='center', verticalalignment='top', fontsize=12)
annotate("Celebrity ad", xy=(214, medianJM[122]-2), xytext=(214.01,
	medianJM[122]-38), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.08, width=0.5, headwidth=4),
	horizontalalignment='center', verticalalignment='top', fontsize=12)
annotate("McCain\nhouses\ngaffe", xy=(234, medianJM[142]+2), xytext=(234.01,
	medianJM[142]+57), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='center', verticalalignment='top', fontsize=12)
annotate("DNC", xy=(238, medianJM[146]+4), xytext=(238.01,
	medianJM[146]+22), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='left', verticalalignment='top', fontsize=12)
annotate("RNC", xy=(246, medianJM[154]-2), xytext=(246.01,
	medianJM[154]-43), textcoords='data', arrowprops=dict(facecolor='darkblue',
	edgecolor='darkblue', shrink=0.075, width=0.5, headwidth=4),
	horizontalalignment='left', verticalalignment='top', fontsize=12)
## End Annotations 

show()
savefig(open('McCain-EV_history.png', 'w'), dpi=62.5, facecolor='#fcfcf4',
		edgecolor='#fcfcf4')

### Sam's adjusted estimate post-RNC

# Sept 1, 4, 5, 8, 9, 11
dates = [245, 248, 249, 252, 253, 255]
est_ev = [343, 324, 311, 238, 265, 238]
ci_low = [324, 287, 278, 200, 232, 200]
ci_high = [362, 353, 342, 270, 296, 270]

plot(dates, est_ev, '-g', linewidth=2)
plot(dates, ci_low, '--g', linewidth=1)
plot(dates, ci_high, '--g', linewidth=1)
### End adjusted estimate

show()
savefig(open('McCain-EV_history-with_adjusted.png', 'w'), dpi=62.5,
		facecolor='#fcfcf4', edgecolor='#fcfcf4')
