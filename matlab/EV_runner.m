%%%  EV_runner.m - a MATLAB script
%%%  Author: Andrew Ferguson <adferguson@alumni.princeton.edu> 
%%%  Script written for election.princeton.edu run by Samuel S.-H. Wang under
%%%  non-commercial-use-only license:
%%%  You may use or modify this software, but only for noncommercial purposes. 
%%%  To seek a commercial-use license, contact sswang@princeton.edu.

% This script simply calls the other MATLAB scripts in appropriate order
% so they can be run in the same MATLAB environment as loaded via the Unix
% script nightly.sh

EV_estimator
EV_jerseyvotes
EV_prediction
% EV_history_plot       % This is commented out because the jbfill routine
                        % crashes MATLAB when running without a display.
                        % Uncomment it to produce the EV history plot in a
                        % graphical environment.

senate_est

quit
