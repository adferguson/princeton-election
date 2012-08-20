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
#    Nov  2, 2008 -- Initial version 
#
############################################################################

import time

import matplotlib
matplotlib.use('Agg')
from pylab import *

hfile = open("../matlab/Sen_histogram.csv")
sen_dist = array([])

for line in hfile:
	try:
		sen_dist = append(sen_dist, float(line[:-1]))
	except ValueError:
		sen_dist = append(sen_dist, float(0.0))

hfile.close()

assert len(sen_dist) == 7 
sen_dist_max = max(sen_dist)

############################################################################
#
# Thumbnail-size graphic, 200px wide, for the right sidebar display
# throughout the blog.
#
############################################################################

subplot(111, axisbelow=True)

bar(arange(56, 63), sen_dist, 1.0, edgecolor='none')

# Draw a red line at 60 seats 
plot((60, 60), (0, sen_dist_max * 1.05), '-r', linewidth=1.5)

xlim(56, 63)
ylim(0, sen_dist_max * 1.05)
xticks(arange(56.5, 63.5, 1), arange(56, 63, 1), fontsize=22)

grid(color='#aaaaaa')

xlabel('Dem/Independent Senate seats', fontsize=26, fontweight='bold');
ylabel('Probability (%)', fontsize=25, fontweight='bold')
title('Senate Seat Outcomes', fontsize=27, fontweight='bold')

label_begins = 4 
label_ends = 6 
max_height_under_label = max(sen_dist[label_begins:label_ends])

text(float(56.5) + label_begins, sen_dist_max * float(0.05)
		+ max_height_under_label, time.strftime("%d-%b\n%I:%M%p %Z"),
		fontsize=21)

show()
savefig(open('Sen_histogram_today-200px.png', 'w'), dpi=25)

clf()

############################################################################
#
# Larger graphic, 500px wide, designed to fit in the center content column.
#
############################################################################

subplot(111, axisbelow=True)

bar(arange(56, 63), sen_dist, 1.0, edgecolor='none')

# Draw a red line at 60 seats
plot((60, 60), (0, sen_dist_max * 1.05), '-r', linewidth=1.5)

xlim(56, 63)
ylim(0, sen_dist_max * 1.05)
xticks(arange(56.5, 63.5, 1), arange(56, 63, 1), fontsize=16)

grid(color='#aaaaaa')

xlabel('Democratic/Independent Senate seats', fontsize=16);
ylabel('Probability of exact # of Seats (%)', fontsize=16)
title('Distribution of Senate Seats', fontsize=18, fontweight='bold')

label_begins = 4 
label_ends = 6 
max_height_under_label = max(sen_dist[label_begins:label_ends])

text(float(56.5) + label_begins, sen_dist_max * float(0.10)
		+ max_height_under_label, time.strftime("%d-%b %I:%M%p %Z"),
		fontsize=14)
text(float(56.5) + label_begins, sen_dist_max * float(0.04) 
		+ max_height_under_label, 'election.princeton.edu', fontsize=14)

show()
savefig(open('Sen_histogram_today.png', 'w'), dpi=62.5, facecolor='#fcfcf4',
		edgecolor='#fcfcf4')
