#!/usr/bin/env python

############################################################################
#
# This Python script retrieves the XML polling feeds donated by Pollster.com
# The feeds are a structured representation of all of the polling data
# publicly accessible through their website. After retreiving the feeds, it
# produces an output file which contains summary statistics for the polling
# in each state (and D.C.), as of each date since April 1. The summary
# statistics are described below under "Output Format".
#
# In other words, the first 51 lines of output are summary statistics (s.s.)
# using all currently available polls (also known as "polls which ended
# before today"). The next 51 lines of output are the same s.s. recomputed,
# but omitting any polls which ended before yesterday. Then, the 51 lines
# of s.s., omitting the polls which ended before two days ago, and so on,
# so that we have the history of these s.s. and can observe the effect of
# new polls.
# 
# Author: Andrew Ferguson <adferguson@alumni.princeton.edu>
#
# Script written for election.princeton.edu run by Samuel S.-H. Wang under
# noncommercial-use-only license:
# You may use or modify this software, but only for noncommericial purposes.
# To seek a commercial-use license, contact sswang@princeton.edu
#
# Update History:
#    Sep 14, 2008 -- Remove "Zogby (Internet)" polls from the dataset
#    Sep 18, 2008 -- No longer skip D.C.; ARG polled it in September
#    Sep 18, 2008 -- Added support for retry if the HTTP socket timed out
#    Sep 30, 2008 -- New rule for choosing polls: use the last seven days
#                    worth of polls if this gives more polls than would be
#                    given by old rule: all at least as young as the 3rd
#                    oldest poll.
#
############################################################################

import sys, urllib2, datetime, time, xml.dom.minidom, socket
from numpy import *

############################################################################
#
# Global configuration and variables
#
############################################################################

output_filename = "polls.median.txt"
midtype = "median"
num_recent_polls_to_use = 3

state_polls = {}

# state_polls is a dictionary with each an entry for each state. Each entry
# is a list of tuples. Each tuple represents one poll and is of the form:
# (margin, start date, end date, mid date, population, polling organization)

############################################################################
#
# Main
#
############################################################################

def main():
	global midtype

	try:
		if sys.argv[1] == "--mean":
			midtype = "mean"
			output_filename = "polls.mean.txt"
	except:
		pass

	for state in state_names:
		state_polls[state] = []

	socket.setdefaulttimeout(5)
	pollster_update()

	# Hard-code 2004 result for D.C. since there is no current polling data
	# until September 2008 and Political analysts do not disagree on the
	# expected outcome.
	state_polls["DC"].append((81, datetime.date(2008, 1, 1),
		datetime.date(2008, 1, 1), datetime.date(2008, 1, 1), 227586,
		"Election 2004"))

	process_polls()


############################################################################
#
# Returns the median and std. error
#
############################################################################

# The std. error is given by:
# 		std. deviation / sqrt(num of polls)
#
# We robustly estimate the std. deviation from the median absolute
# deviation (MAD) using the standard formula:
#		std. deviation =  MAD / invcdf(0.75)
#
# The MAD is defined as median( abs[samples - median(samples)] )
# invcdf(0.75) is approximately 0.6745

def get_statistics(set):
	[margins, sdates, edates, mdates, pop, poll_orgs] = zip(*set)
	set = array(margins)

	num = set.size
	assert num >= 3

	if midtype == "median":
		median_margin = median(set)
		mad = median(abs(set - median_margin))
		sem_est = mad/0.6745/sqrt(num)

		return (median_margin, sem_est)

	else:
		assert midtype == "mean"

		mean_margin = mean(set)
		sem = std(set) / sqrt(num)

		return (mean_margin, sem)

# Special case for when only two polls are available

def get_two_statistics(set):
	[margins, sdates, edates, mdates, pop, poll_args] = zip(*set)
	set = array(margins)

	assert set.size == 2

	mean_margin = mean(set)
	sem = max(std(set) / sqrt(set.size), 3)

	return (mean_margin, sem)


############################################################################
#
# Functions to write the statistics which Sam's MATLAB scripts will use as
# inputs. There is one line of statistics for each state and D.C., for
# each date from today back to April 1
#
############################################################################

# Output Format -- 5 numbers per state
#	- number of polls used for average
#	- middle date of oldest poll used (January 1= 1)
#	- average margin where margin>0 is Obama ahead of McCain
#	- estimated SEM of margin
#	- analysisdate

# Remember, the format of the tuple for each list:
# (margin, start date, end date, mid date, pop, polling organization)

def write_statistics(pfile, polls):
	# Number of polls available on this date for this state
	num = len(polls)

	if num == 0:
		assert False
	elif num == 1:
		pfile.write("%s " % num)
		pfile.write("%s " % int(polls[0][3].strftime("%j")))
		pfile.write("%s " % polls[0][0])
		pfile.write("%s " % sqrt(1.0/polls[0][4]))
	elif num == 2:
		pfile.write("%s " % num)
		pfile.write("%s " % int(polls[1][3].strftime("%j")))
		pfile.write("%s %s " % get_two_statistics(polls))
	else:
		# We want to use only the three most recent polls, as defined by the
		# midpoint date, and allowing for ties
		polls.sort(key=lambda x: x[3], reverse=True)
		third_date = polls[num_recent_polls_to_use - 1][3]
		last_three = filter(lambda x: x[3] >= third_date, polls)

		# Or, if this gives more polls, use the polls from the 7 days prior
		# to the most recent poll.
		polls.sort(key=lambda x: x[3], reverse=True)
		most_recent_date = polls[0][3]
		seven_days_prior = most_recent_date - datetime.timedelta(7, 0, 0)
		last_seven_days = filter(lambda x: x[3] >= seven_days_prior, polls)

		if (len(last_seven_days) > len(last_three)):
			working_subset = last_seven_days
		else:
			working_subset = last_three

		pfile.write("%s " % len(working_subset))
		pfile.write("%s " % int(working_subset[-1][3].strftime("%j")))
		pfile.write("%s %s " % get_statistics(working_subset))


def process_polls():
	pfile = open(output_filename, "w")

	# Make sure the polls are sorted with most recent first
	for state in state_polls.keys():
		polls = state_polls[state]
		polls.sort(key=lambda x: x[2], reverse=True)

	# Write the 51 lines of output statistics for each day, from now
	# back to April 1
	for day in campaign_season():
		for state in sorted(state_names, key=lambda x: state_names[x]):
			polls = state_polls[state]

			polls_ended_before_day = filter(lambda x: x[2] < day, polls)

			# XXX cleaning:
			#  reject two polls by the same pollster if their
			# [startdate,enddate] intervals overlap (i.e. if older
			# enddate>=newer startdate).

			write_statistics(pfile, polls_ended_before_day)
			pfile.write("%s\n" % int(day.strftime("%j")))

	pfile.close()


############################################################################
#
# Functions to gather poll data from pollster.com. Adds tuples of
# the form (margin, end_date) to the state_polls dictionary. The margin
# is defined as: Dem - GOP
#
############################################################################

def pollster_update():

	# The Pollster.com XML feeds are password-protected. We store
	# the username and password in a separate file for security.

	pollster_config = open(".pollster.pwd")
	username = pollster_config.readline()[:-1]
	passwd = pollster_config.readline()[:-1]
	pollster_base_url = pollster_config.readline()[:-1]
	pollster_config.close()

	pollster_dir = pollster_base_url.rsplit("/", 1)[0]

	passwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	auth_handler = urllib2.HTTPBasicAuthHandler(passwd_mgr)
	auth_handler.add_password(realm=None,
							  uri=pollster_dir,
							  user=username,
							  passwd=passwd)
	opener = urllib2.build_opener(auth_handler)
	urllib2.install_opener(opener)

	# Process the XML feed for each state

	for state in sorted(state_names, key=lambda x: state_names[x]):
		success = False
		tries = 0
		while not success:
			try:
				f = urllib2.urlopen(pollster_base_url % state)
				success = True
			except urllib2.URLError:
				if tries < 3:
					tries += 1
					time.sleep(2)
				else:
					print "FAIL on state %s (tried three times)" % state
					sys.stdout.flush()
					raise

		pollster_parse(state, f)
	
# Parses an XML document which has information about all of the polls for
# the given state. Each poll has an entry like:
#
# <n state="WA" pollster="SurveyUSA" partisan="0" sdate="07/13/2008"
#     edate="07/15/2008" pop="666" vtype="LV" mode="IVR" mccain="39" obama="55"
#     barr="-" nader="-" other="-" undecided="6" id="1"/>

def pollster_parse(state, file):
	# First, fix Pollster.com's malformed XML
	contents = file.read()
	contents = contents.replace("&", "&amp;")

	# Then grab all of the polls
	xmldoc = xml.dom.minidom.parseString(contents)
	polls = xmldoc.getElementsByTagName("n")

	for poll in polls:
		margin = int(poll.attributes["obama"].value) \
					- int(poll.attributes["mccain"].value)
		start_date = strpdate(poll.attributes["sdate"].value)
		end_date = strpdate(poll.attributes["edate"].value)
		mid_date = start_date + ((end_date - start_date) / 2)
		poll_org = str(poll.attributes["pollster"].value)
		try:
			pop = int(poll.attributes["pop"].value)
		except ValueError:
			pop = 0 # Sometimes, Pollster.com does not report the sample size

		if poll_org != "Zogby (Internet)":
			state_polls[state].append((margin, start_date, end_date,
									   mid_date, pop, poll_org))


############################################################################
#
# Utility functions and data
#
############################################################################

# Parses a date_string into a datetime.date. Included here to support
# Python 2.4, which lacks datetime.datetime.strpdate()

def strpdate(date_string, format="%m/%d/%Y"):
	return datetime.date(*(time.strptime(date_string, format)[0:3]))

# Generates all of the dates in the general election campaign season,
# starting from today and working back to April 1st

def campaign_season():
	day = datetime.date.today()
	start = datetime.date(2008, 4, 1)

	while day >= start:
		yield day
		day = day - datetime.timedelta(1, 0, 0)

state_names = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'D.C.',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    }

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass
