#!/bin/bash

############################################################################
#
# This script is used to regenerate the history of EV estimates
#
# Author: Andrew Ferguson <adferguson@alumni.princeton.edu>
#
# Script written for election.princeton.edu run by Samuel S.-H. Wang under
# noncommercial-use-only license:
# You may use or modify this software, but only for noncommericial purposes.
# To seek a commercial-use license, contact sswang@princeton.edu
#
############################################################################

HISTORY=EV_estimate_history.csv

#MATLAB_PATH="/raid/software/matlab-7.1/bin"
MATLAB_PATH="/local/bin"

#SRC_PATH="/home/election"
SRC_PATH="/home/adf/pec/princeton-election"

cd $SRC_PATH/matlab
rm $HISTORY
touch $HISTORY

cd $SRC_PATH/python/
./update_polls.py

cd ..
mv -f python/polls.median.txt bin/polls.median.txt
cd bin

last_day=$((`wc -l polls.median.txt | cut -d\  -f 1` / 51))
day=1

while [ $day -le $last_day ]; do
    amount=$((day*51))
    echo "Day: $day, Amount: $amount"

	tail -$amount polls.median.txt > $SRC_PATH/matlab/polls.median.txt

	cd $SRC_PATH/matlab/
	$MATLAB_PATH/matlab -nodisplay -nojvm -r EV_runner 2>&1 > /dev/null
    cd $SRC_PATH/bin/

	day=$((day+1))
done

rm polls.median.txt
