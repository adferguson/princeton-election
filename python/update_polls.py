#!/usr/bin/python

############################################################################
#
# This Python script retrieves the XML polling feeds from Huffington Post
# The feeds are a structured representation of all of the polling data
# publicly accessible through their website. After retreiving the feeds, it
# produces an output file which contains summary statistics for the polling
# in each state (and D.C.), as of each date since May 22. The summary
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
#    Aug 19, 2012 -- moved to GitHub; future updates in commit messages
#    Jul 10, 2012 -- Updated for new HuffPo XML format
#    Jul  8, 2012 -- Export CSV files for exploratory analysis
#    Jul  7, 2012 -- Initial port from 2008 version
#    
############################################################################

import os, sys, urllib2, datetime, time, xml.dom.minidom, socket
from numpy import *

############################################################################
#
# Global configuration and variables
#
############################################################################

output_filename = "polls.median.txt"
midtype = "median"
num_recent_polls_to_use = 3
huffpo_base_url = ""
huffpo_childNodes_per_page = 21 # 10 polls per page, plus space childNode on either side
archive_dir = "archive/"

state_polls = {}
# state_polls is a dictionary with each an entry for each state. Each entry
# is a list of tuples. Each tuple represents one poll and is of the form:
# (margin, start date, end date, mid date, population, polling organization)

poll_ids = []
max_filenum = 0

# Files for exploratory analysis
state_filename = "2012_StatePolls.csv"
state_file = None
national_filename = "2012_NationalPolls.csv"
national_file = None

############################################################################
#
# Main
#
############################################################################

def main():
    global max_filenum
    global midtype
    global output_filename
    global huffpo_base_url
    global state_file, national_file

    try:
        if sys.argv[1] == "--mean":
            midtype = "mean"
            output_filename = "polls.mean.txt"
    except:
        pass

    for state in state_names:
        state_polls[state] = []

    state_file = init_analysis_file(state_filename)
    national_file = init_analysis_file(national_filename)
    
    # load base url
    huffpo_config = open(".huffpo.url")
    huffpo_base_url = huffpo_config.readline()[:-1]
    huffpo_config.close()

    # process archive of polls
#    for fname in os.listdir(archive_dir):
#        n = int(fname.split(".")[0])
#        if n > max_filenum:
#            max_filenum = n
#        parse_pollfile(archive_dir + fname)

    # get the latest polls
    socket.setdefaulttimeout(5)
    fetch_latest_polls()

    add_2008_results()
    process_polls()

    state_file.close()
    national_file.close()


def init_analysis_file(filename):
    outfile = open(filename, "w+")

    outfile.write("State,pollster,pop,vtype,method,begmm,begdd,begyy,")
    outfile.write("endmm,enddd,endyy,romeny,obama,other,undecided,")
    outfile.write("Begdate,Enddate,Middate\n")

    return outfile


############################################################################
#
# Returns the median and std. error
#
############################################################################

# The std. error is given by:
#         std. deviation / sqrt(num of polls)
#
# We robustly estimate the std. deviation from the median absolute
# deviation (MAD) using the standard formula:
#        std. deviation =  MAD / invcdf(0.75)
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
# each date from today back to May 22
#
############################################################################

# Output Format -- 5 numbers per state
#    - number of polls used for average
#    - middle date of oldest poll used (January 1= 1)
#    - average margin where margin>0 is Obama ahead of Romney
#    - estimated SEM of margin
#    - analysisdate

# Remember, the format of the tuple for each list:
# (margin, start date, end date, mid date, pop, polling organization)

def write_statistics(pfile, polls):
    # Number of polls available on this date for this state
    num = len(polls)

    if num == 0:
        assert False # TODO(adf): here, grab the 2008 results!
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
    # back to May 22
    for day in campaign_season():
        for state in sorted(state_names, key=lambda x: state_names[x]):
            polls = state_polls[state]

            polls_ended_before_day = filter(lambda x: x[2] < day, polls)

            # XXX cleaning:
            #  reject two polls by the same pollster if their
            # [startdate,enddate] intervals overlap (i.e. if older
            # enddate>=newer startdate).

            if len(polls_ended_before_day) == 0:
                print "debug info: %s, %d" % (state, day)

            write_statistics(pfile, polls_ended_before_day)
            pfile.write("%s\n" % int(day.strftime("%j")))

    pfile.close()

############################################################################
#
# Functions to fetch the latest polls from the Huffington Post
#
############################################################################


def url_fetcher(page_num):
    tries = 0
    while True:
        try:
            f = urllib2.urlopen(huffpo_base_url + str(page_num))
            return f
        except urllib2.URLError:
            if tries < 3:
                tries += 1
                time.sleep(2)
            else:
                print "FAIL on page %d (tried three times)" % page_num
                sys.stdout.flush()
                raise


def fetch_latest_polls():
    global max_filenum
    stop = False
    page_num = 0

    while (not stop):
        page_num += 1
        print "Fetching page: " + str(page_num)
        page = url_fetcher(page_num)

        xmldoc = parse_pollfile(page)
        xmldoc.childNodes[0].normalize()

        if len(xmldoc.childNodes[0].childNodes) > 1:
            max_filenum += 1
            f = open(archive_dir + str(max_filenum) + ".xml", 'w')
            xmldoc.writexml(f)
            f.close()

        if len(xmldoc.childNodes[0].childNodes) == 0:
            stop = True
        else:
            time.sleep(1)


############################################################################
#
# Functions to process poll data from Huffington Post. Adds tuples of
# the form (margin, start_date, end_date, mid_date, pop, poll_org) to the
# state_polls dictionary. The margin is defined as: Dem - GOP
#
############################################################################


def parse_pollfile(filename):
    xmldoc = unique_polls(filename)
    process_pollfile(xmldoc)
    return xmldoc


def unique_polls(filename):
    xmldoc = xml.dom.minidom.parse(filename)
    
    pi_nodes = xmldoc.getElementsByTagName("id")
    
    for pi_node in pi_nodes:
        poll_id = int(pi_node.childNodes[0].nodeValue)

        if poll_id in poll_ids:
            poll_node = pi_node.parentNode
            polls = poll_node.parentNode
            polls.removeChild(poll_node)
        else:
            poll_ids.append(poll_id)
    
    return xmldoc


def get_opt_subelem(elem, name, default):
    tmp = elem.getElementsByTagName(name)
    if len(tmp) > 0 and tmp[0].hasChildNodes():
        return tmp[0].childNodes[0].nodeValue
    return default


def subpop_parse(subpop):
    values = {"Obama":"", "Romney":"", "Other":"", "Undecided":""}

    vtype = get_opt_subelem(subpop, "name", "")
    pop = int(get_opt_subelem(subpop, "observations", "0"))

    responses = subpop.getElementsByTagName("response")

    for r in responses:
        candidate = r.getElementsByTagName("choice")[0].childNodes[0].nodeValue
        value = r.getElementsByTagName("value")[0].childNodes[0].nodeValue
        values[candidate] = value
        
    assert(values["Obama"] != "")
    assert(values["Romney"] != "")

    return (vtype, pop, values)


def process_subpop(poll_org, method, state, start_date, end_date, subpop):
    global state_file, national_file

    (vtype, pop, values) = subpop_parse(subpop)

    mid_date = start_date + ((end_date - start_date) / 2)
    margin = int(values["Obama"]) - int(values["Romney"]) 
    f = None

    if state != "US":
        state_polls[state].append((margin, start_date, end_date,
                                   mid_date, pop, poll_org))
        f = state_file
    else:
        f = national_file

    d = (start_date.month, start_date.day,start_date.year,
         end_date.month, end_date.day, end_date.year,
         mid_date.month, mid_date.day, mid_date.year)
    f.write("%s,\"%s\",%d,\"%s\",\"%s\"," % (state, poll_org, pop, vtype, method))
    f.write("%d,%d,%d,%d,%d,%d," % d[:6])
    f.write("%s,%s,%s,%s," % (values["Romney"], values["Obama"],
        values["Other"], values["Undecided"]))
    f.write("%s/%s/%s,%s/%s/%s,%s/%s/%s\n" % d)


def process_pollfile(xmldoc):
    topics = xmldoc.getElementsByTagName("topic")
    
    presTopics = filter(lambda x: x.hasChildNodes() and 
            x.childNodes[0].nodeValue=="2012-president", topics)

    questions = map(lambda x: x.parentNode, presTopics)

    for q in questions:
        poll = q.parentNode.parentNode
        poll_org = poll.getElementsByTagName("pollster")[0].childNodes[0].nodeValue
        method = get_opt_subelem(poll, "method", "")
        state = q.getElementsByTagName("state")[0].childNodes[0].nodeValue
        start_date = strpdate(poll.getElementsByTagName("start_date")[0].childNodes[0].nodeValue)
        end_date = strpdate(poll.getElementsByTagName("end_date")[0].childNodes[0].nodeValue)

        subpops = q.getElementsByTagName("subpopulation")

        if len(subpops) >= 2:
            for subpop in subpops:
                vtype = get_opt_subelem(subpop, "name", "")
                if vtype == "Likely Voter":
                    process_subpop(poll_org, method, state, start_date, end_date, subpop)
        else:
            for subpop in subpops:
                process_subpop(poll_org, method, state, start_date, end_date, subpop)


############################################################################
#
# Utility functions and data
#
############################################################################

# Parses a date_string into a datetime.date. Included here to support
# Python 2.4, which lacks datetime.datetime.strpdate()

def strpdate(date_string, format="%Y-%m-%d"):
    return datetime.date(*(time.strptime(date_string, format)[0:3]))


# Generates all of the dates in the general election campaign season,
# starting from today and working back to May 22nd

def campaign_season():
    day = datetime.date.today()
    start = datetime.date(2012, 5, 22)

    while day >= start:
        yield day
        day = day - datetime.timedelta(1, 0, 0)


# TODO(adf): we should do something smart with these states when they
# DO get a result ... put them in a separate data structure and look-up above
#
# Hard-code 2008 results for several states since there is no current
# polling data and Political analysts do not disagree on the expected outcome.

def add_2008_results():
    state_polls["DC"].append((86, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 265853,
        "Election 2008"))
    state_polls["AL"].append((-22, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 2099819,
        "Election 2008"))
    state_polls["AK"].append((-22, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 326197,
        "Election 2008"))
    state_polls["DE"].append((25, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 412412,
        "Election 2008"))
    state_polls["HI"].append((45, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 453568,
        "Election 2008"))
    state_polls["ID"].append((-25, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 655032,
        "Election 2008"))
    state_polls["KS"].append((-15, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 1235872,
        "Election 2008"))
    state_polls["KY"].append((-16, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 1826508,
        "Election 2008"))
    state_polls["LA"].append((-19, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 1960761,
        "Election 2008"))
    state_polls["MS"].append((-13, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 2925205,
        "Election 2008"))
    state_polls["RI"].append((28, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 469767,
        "Election 2008"))
    state_polls["UT"].append((-28, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 952370,
        "Election 2008"))
    state_polls["WV"].append((-13, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 713451,
        "Election 2008"))
    state_polls["WY"].append((-32, datetime.date(2012, 1, 1),
        datetime.date(2012, 1, 1), datetime.date(2012, 1, 1), 254658,
        "Election 2008"))


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
