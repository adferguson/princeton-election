%%%  EV_jerseyvotes.m - a MATLAB script
%%%  Copyright 2008 by Samuel S.-H. Wang
%%%  Noncommercial-use-only license: 
%%%  You may use or modify this software, but only for noncommercial purposes. 
%%%  To seek a commercial-use license, contact the author at sswang@princeton.edu.
%%%
%%%  Updated by Andrew Ferguson on Oct 8, 2008 to ensure that at least ten
%%%  states are displayed.

% Likelihood analysis of all possible outcomes of election based 
% on the meta-analytical methods of Prof. Sam Wang, Princeton University.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% EV_jerseyvotes.m
% 
% This script assumes that EV_estimator has just been run!!!
% This script generates 1 CSV file:
% 
% jerseyvotes.csv
%    The file has the same number of lines as the number of uncertain
%    states. These are not necessarily the same states.
%    Each line has 3 fields:
%       - the index number of a state
%       - its two-letter postal abbreviation
%       - the power of a voter in that state to influence the overall
%           election outcome, normalized to a voter in NJs
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% biaspct=0;
if metamargin>-999
    biaspct=-metamargin; % changed on 8/8/08 to reflect discussion w/reader James
end
EV_median
midpoint=cumulative_prob(min(find(electoralvotes>=269)));

for state=1:num_states
    polls.margin(state)=polls.margin(state)-0.1;
    EV_median
    probability_GOP_win=cumulative_prob(min(find(electoralvotes>=269)));
    difference(state)=(probability_GOP_win-midpoint)*10000;
    polls.margin(state)=polls.margin(state)+0.1;
end

kvoters=[1883 313 2013 1055 12422 2130 1579 375 228 7610 3302 429 598 5274 2468 1507 1188 1796 1943 741 2387 2912 4839 2828 1152 2731 450 778 830 678 3612 756 7391 3501 313 5628 1464 1837 5770 437 1618 388 2437 7411 928 312 3198 2859 756 2997 243];
jerseyvotes=difference./kvoters;

% jerseyvotes=jerseyvotes/jerseyvotes(31); % gives exact ratios
% jerseyvotes=round(10*jerseyvotes/jerseyvotes(31))/10; % gives tenths
% jerseyvotes=roundn(jerseyvotes,floor(log10(jerseyvotes))-1); % gives top two significant figures

jerseyvotes=100*jerseyvotes/max(jerseyvotes); 
% normalizes to the most powerful state, which is defined as 100; see
% discussion 8/8/08 with James

for i=1:num_states
    if i~=31
        jerseyvotes(i)=roundn(jerseyvotes(i),-1);
    end
end
% round everything but NJ itself to the nearest tenth

[foo, ijersey]=sort(jerseyvotes);
display_num=max(size(uncertain,2), 10);
display_num=51

if exist('jerseyvotes.csv','file')
        delete('jerseyvotes.csv')
end
for i=num_states:-1:(num_states-display_num+1)
    foo=[num2str(ijersey(i)) ',' statename(ijersey(i)) ',' num2str(jerseyvotes(ijersey(i))) ];
    dlmwrite('jerseyvotes.csv',foo,'-append','delimiter','')
end
%foo=[num2str(31) ',' statename(31) ',' num2str(jerseyvotes(31)) ];
%dlmwrite('jerseyvotes.csv',foo,'-append','delimiter','')
