#!/bin/sh

############################################################################
#
# This script is run at 12:01am each morning by the Unix cron daemon to
# update the site. It first uses the Python update_polls.py script to
# prepare the summary statistics which are used by the MATLAB scripts it
# calls next. Then, it updates the automatically generated text and graphics
# which display the calculations using additional Python scripts.
#
# Author: Andrew Ferguson <adferguson@alumni.princeton.edu>
#
# Script written for election.princeton.edu run by Samuel S.-H. Wang under
# noncommercial-use-only license:
# You may use or modify this software, but only for noncommericial purposes.
# To seek a commercial-use license, contact sswang@princeton.edu
#
############################################################################

cd ~/python/
rm archive/*.xml
./update_polls.py

cd ..
mv -f python/polls.median.txt matlab/polls.median.txt

cd matlab
tail -2 EV_estimate_history.csv
/raid/software/matlab-7.1/bin/matlab -nodisplay -nojvm -r EV_runner 2>&1 > /dev/null
tail -2 EV_estimate_history.csv
ls -l EV_estimate_history.csv

cd ../python
./current_ev.py
./histogram.py
./history_plot.py
./jerseyvotes.py
./ev_map.py
./metamargin_history_plot.py
#./sen_current.py     # Added Nov. 2, 2008
#./sen_histogram.py   # Added Nov. 2, 2008

# Temporary change to how 500px wide EV_history plot is resized
# Oct. 3, 2008
mv EV_history.png EV_history-subsample_resize.png
convert -resize 500x500 EV_history-full_size.png EV_history.png

cd ..
mv -f python/*.html autotext/
mv -f python/*.txt autotext/
mv -f python/*.png autographics/
mv -f python/*.csv private/
mv -f python/ev_map_runner.sh bin/
chmod a+x bin/ev_map_runner.sh

cd java
../bin/ev_map_runner.sh
../bin/ev_map_postprocess.sh

cd ..
mv -f java/*.png autographics/
