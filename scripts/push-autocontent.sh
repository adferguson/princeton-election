#!/bin/bash

#SRC_PATH="/home/election"
SRC_PATH="/home/adf/pec/princeton-election"

cd $SRC_PATH/autographics
scp *.png swang@synapse.princeton.edu:/var/www/html/autographics/

cd $SRC_PATH/autotext
scp *.html swang@synapse.princeton.edu:/var/www/html/autotext/

cd $SRC_PATH/matlab
scp *.csv swang@synapse.princeton.edu:/var/www/html/code/matlab/
