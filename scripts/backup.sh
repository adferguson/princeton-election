#!/bin/sh

############################################################################
#
# This script is run at 4:00pm each afternoon by the Unix cron daemon to
# produce a backup of the WordPress database. It deletes any backup copies
# that are more than one week old.
#
# Author: Andrew Ferguson <adferguson@alumni.princeton.edu>
#
# Script written for election.princeton.edu run by Samuel S.-H. Wang under
# noncommercial-use-only license:
# You may use or modify this software, but only for noncommericial purposes.
# To seek a commercial-use license, contact sswang@princeton.edu
#
# Update History:
#      Feb 8, 2009 -- Fix matching patterns to support new year (2009) 
#
############################################################################

cd ~/db-backup/

mysqldump election | gzip > election-`date +%F`.sql.gz

num_backups=`ls -1 election-????-??-??.sql.gz | wc -l`

if [ $num_backups -gt 7 ] ; then
	num_delete=`expr $num_backups - 7`
	ls -1 election-????-??-??.sql.gz | head -$num_delete | xargs rm -f
fi
