#!/usr/bin/env python

############################################################################
#
# This script produces the histogram graphics for the distribution of
# possible Obama electoral votes. The distribution is calculated by the
# MATLAB scripts EV_estimator.m and EV_median.m. The histogram is also
# plotted by those scripts for stand-alone display, but we redraw them with
# Python's matplotlib for better web display.
#
# Author: Andrew Ferguson <adferguson@alumni.princeton.edu>
#
# Script written for election.princeton.edu run by Samuel S.-H. Wang under
# noncommercial-use-only license:
# You may use or modify this software, but only for noncommericial purposes.
# To seek a commercial-use license, contact sswang@princeton.edu
#
# Update History:
#    Jul  7, 2012 -- Update for 2012 election
#    Oct  4, 2008 -- Draw the outer 5% of the histogram in mint green to
#                    better display the 95% Confidence Interval
#    Oct  8, 2008 -- Adjust edges of histogram to reflect current EV counts
#
############################################################################

import time

import matplotlib
matplotlib.use('Agg')
from pylab import *

hfile = open("../matlab/EV_histogram.csv")
ev_dist = array([])

for line in hfile:
	try:
		ev_dist = append(ev_dist, float(line[:-1]))
	except ValueError:
		ev_dist = append(ev_dist, float(0.0))

hfile.close()

assert len(ev_dist) == 538
ev_dist_max = max(ev_dist)

# Get the boundaries for the 95% Confidence Interval

efile = open("../matlab/EV_estimates.csv")
values = efile.read()[:-1].split(",")
efile.close()

low95bound = int(values[9])
high95bound = int(values[10])

############################################################################
#
# Thumbnail-size graphic, 200px wide, for the right sidebar display
# throughout the blog.
#
############################################################################

subplot(111, axisbelow=True)

# Split the histogram so that the outer 5% (2.5% on each side) are drawn
# in mint green
bar(arange(low95bound-1), ev_dist[:low95bound-1] * float(100.0), 1.0,
		color="#8bd98b", edgecolor='#8bd98b')
bar(arange(low95bound-1, high95bound), ev_dist[low95bound-1:high95bound]
		* float(100.0), 1.0, edgecolor='blue')
bar(arange(high95bound, 538), ev_dist[high95bound:] * float(100.0), 1.0,
		color="#8bd98b", edgecolor='#8bd98b')

# Draw a red line at 269 EV
plot((269, 269), (0, ev_dist_max * 105), '-r', linewidth=1.5)

xlim(220, 400)
ylim(0, ev_dist_max * 105)
xticks(arange(220, 420, 20))

grid(color='#aaaaaa')

xlabel('Obama EV', fontsize=26, fontweight='bold');
ylabel('Probability (%)', fontsize=25, fontweight='bold')
title('All possible outcomes', fontsize=27, fontweight='bold')

text(223, ev_dist_max * 95, 'Romney', fontsize=24, fontweight='bold')
text(223, ev_dist_max * 88, 'wins', fontsize=24, fontweight='bold')
text(223, ev_dist_max * 79, 'today', fontsize=24, fontweight='bold')
text(365, ev_dist_max * 95, 'Obama', fontsize=24, fontweight='bold')
text(377, ev_dist_max * 88, 'wins', fontsize=24, fontweight='bold')
text(372, ev_dist_max * 79, 'today', fontsize=24, fontweight='bold')

label_begins = 222
label_ends = 280
max_height_under_label = max(ev_dist[label_begins:label_ends]) * 100

text(label_begins, ev_dist_max * 5 + max_height_under_label,
		time.strftime("%d-%b\n%I:%M%p %Z"), fontsize=21)

show()
savefig(open('EV_histogram_today-200px.png', 'w'), dpi=25)

clf()

############################################################################
#
# Larger graphic, 500px wide, designed to fit in the center content column.
#
############################################################################

subplot(111, axisbelow=True)

# Split the histogram so that the outer 5% (2.5% on each side) are drawn
# in mint green
bar(arange(low95bound-1), ev_dist[:low95bound-1] * float(100.0), 1.0,
		color="#8bd98b", edgecolor='#8bd98b')
bar(arange(low95bound-1, high95bound), ev_dist[low95bound-1:high95bound]
		* float(100.0), 1.0, edgecolor='blue')
bar(arange(high95bound, 538), ev_dist[high95bound:] * float(100.0), 1.0,
		color="#8bd98b", edgecolor='#8bd98b')

# Draw a red line at 269 EV
plot((269, 269), (0, ev_dist_max * 105), '-r', linewidth=1.5)

xlim(220, 400)
ylim(0, ev_dist_max * 105)
xticks(arange(220, 420, 20))

grid(color='#aaaaaa')

xlabel('Electoral votes for Obama', fontsize=16);
ylabel('Probability of exact # of EV (%)', fontsize=16)
title('Distribution of all possible outcomes', fontsize=18, fontweight='bold')

text(223, ev_dist_max * 99, 'Romney wins', fontsize=16, fontweight='bold')
text(223, ev_dist_max * 93, 'today', fontsize=16, fontweight='bold')
text(355, ev_dist_max * 99, 'Obama wins', fontsize=16, fontweight='bold')
text(379, ev_dist_max * 93, 'today', fontsize=16, fontweight='bold')

label_begins = 222
label_ends = 285
max_height_under_label = max(ev_dist[label_begins:label_ends]) * 100

text(label_begins, ev_dist_max * 13 + max_height_under_label,
		time.strftime("%d-%b %I:%M%p %Z"), fontsize=14)
text(label_begins, ev_dist_max * 7  + max_height_under_label,
		'election.princeton.edu', fontsize=14)

show()
savefig(open('EV_histogram_today.png', 'w'), dpi=62.5, facecolor='#fcfcf4',
		edgecolor='#fcfcf4')
