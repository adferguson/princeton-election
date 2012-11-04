#!/bin/bash

#SRC_PATH="/home/election"
SRC_PATH="/home/adf/pec/princeton-election"

cd $SRC_PATH/autographics
scp *.png swang@synapse.princeton.edu:/var/www/html/autographics/
scp *.png election@quanto.cs.brown.edu:/home/election/autographics/

cd $SRC_PATH/autotext
scp *.html swang@synapse.princeton.edu:/var/www/html/autotext/
cd ../python
./current_ev-2.py
mv current_ev.html ../autotext
cd ../autotext
scp *.html election@quanto.cs.brown.edu:/home/election/autotext/

cd $SRC_PATH/matlab
scp *.csv swang@synapse.princeton.edu:/var/www/html/code/matlab/
scp *.csv election@quanto.cs.brown.edu:/home/election/matlab/

cd $SRC_PATH/python/processed
scp *.csv swang@synapse.princeton.edu:/var/www/html/code/python/processed/
scp *.csv election@quanto.cs.brown.edu:/home/election/python/processed/

