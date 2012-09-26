%%%  EV_estimator.m - a MATLAB script
%%%  Copyright 2008 by Samuel S.-H. Wang
%%%  Noncommercial-use-only license: 
%%%  You may use or modify this software, but only for noncommercial purposes. 
%%%  To seek a commercial-use license, contact the author at sswang@princeton.edu.

% Likelihood analysis of all possible outcomes of election based 
% on the meta-analytical methods of Prof. Sam Wang, Princeton University.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% EV_estimator.m
% 
% This script loads 'poll.median.txt' and generates or updates/replaces 4 CSV files:
% 
% EV_estimates.csv
%    all in one line:
%    2 values - medianEV for the two candidates, where a margin>0 favors the first candidate (in our case, Obama);
%    2 values - modeEV for the two candidates;
%    3 values - assigned (>95% prob) EV for each candidate, with a third entry for undecided;
%    4 values - confidence intervals for candidate 1's EV: +/-1 sigma, then
%    95% band; and
%    1 value - number of state polls used to make the estimates.
%    1 value - (calculated by EV_metamargin and appended) the meta-margin.
% 
% Another file, EV_estimate_history, is updated with the same
% information as EV_estimates.csv plus 1 value for the date.
%
% stateprobs.csv
%    A 51-line file giving percentage probabilities for candidate #1 win of the popular vote, state by state. 
%    Note that for EV calculation, NE and ME were assumed to have a winner-take-all rule, but in fact they do not. 
%    Because in practice NE and ME have not split their votes, for now this is a satisfactory approximation.
%    The second field on each line is the current median polling margin.
%    The third field on each line is the two-letter postal abbreviation.
% 
% EV_histogram.csv
%    A 538-line file giving the probability histogram of each EV outcome. Line 1 is 
%    the probability of candidate #1 (Obama) getting 1 EV. Line 2 is 2 EV, and so on. 
%    Note that 0 EV is left out of this histogram for ease of indexing.
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% This routine expects the global variables biaspct and analysisdate

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%% Initialize variables %%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

polls.state=[
 'AL,AK,AZ,AR,CA,CO,CT,DC,DE,FL,GA,HI,ID,IL,IN,IA,KS,KY,LA,ME,MD,MA,MI,MN,MS,MO,MT,NE,NV,NH,NJ,NM,NY,NC,ND,OH,OK,OR,PA,RI,SC,SD,TN,TX,UT,VT,VA,WA,WV,WI,WY '];
polls.EV=[9 3 11 6 55 9 7 3 3 29 16 4 4 20 11 6 6 8 8 4 10 11 16 10 6 10 3 5 6 4 14 5 29 15 3 18 7 7 20 4 9 3 11 38 6 3 13 12 5 10 3 ];
num_states=size(polls.EV,2);

assignedEV(3)=sum(polls.EV);
assignedEV(1)=0; assignedEV(2)=0; % do not assume any states are safe - calculate all 2^51 possibilities!
% 1=Dem, 2=GOP, 3=uncertain
% checksum to make sure no double assignment or missed assignment
if (sum(assignedEV)~=538)
    warning('Warning: Electoral votes do not sum to 538!')
    assignedEV
end

if ~exist('biaspct','var')
    biaspct=0;
end
forhistory=biaspct==0;

if ~exist('analysisdate','var')
    analysisdate=0;
end

if ~exist('metacalc','var')
    metacalc=1;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%% Load and parse polling data %%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
polldata=load('polls.median.txt');
numlines = size(polldata,1);
if mod(numlines,51)>0
    warning('Warning: polls.median.txt is not a multiple of 51 lines long');
end
% Currently we are using median and effective SEM of the last 3 polls.
% To de-emphasize extreme outliers, in place of SD we use (median absolute deviation)/0.6745

% find the desired data within the file
if analysisdate>0  && numlines>51
    foo=find(polldata(:,5)==analysisdate,1,'first');
%    ind=min([size(polldata,1)-50 foo']);
    foo2=find(polldata(:,5)==max(polldata(:,5)),1,'first');
    ind=max([foo2 foo]); %assume reverse time order
    polldata=polldata(ind:ind+50,:);
    clear foo2 foo ind
elseif numlines>51
%    polldata = polldata(numlines-50:numlines,:);
    polldata = polldata(1:51,:);
end

% Use statistics from data file
polls.margin=polldata(:,3)';
polls.SEM=polldata(:,4)';
polls.SEM=max(polls.SEM,zeros(1,51)+2);
totalpollsused=sum(polldata(:,1))-1; % assume DC has no polls

% mock data in case we ever need to do a dry run
% Use three poll (as of 23 July)
%polls.margin=[-14 -7 -10 -10 24 7 20 81 9 -2 -9 30 -13 13 1 10 -20 -16 -19 10 13 16 5 18 -6 0 5 -16 2 3 11 5 13 -4 0 -6 -14 9 4 24 -9 -4 -15 -9 -24 34 0 12 -8 11 -13];
%polls.SEM=zeros(1,51)+3;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%% Where the magic happens! %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
EV_median

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%% Plot the histogram %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
close
phandle=plot([269 269],[0 max(histogram)*105],'-r','LineWidth',1.5);
EVticks=200:20:380;
grid on
hold on
bar(histogram*100)
axis([200 380 0 max(histogram)*105])
xlabel('Electoral votes for Obama','FontSize',14);
ylabel('Probability of exact # of EV (%)','FontSize',14)
set(gcf, 'InvertHardCopy', 'off');
title('Distribution of all possible outcomes','FontSize',14)
text(203,max(histogram)*99,'Romney wins','FontSize',14)
text(335,max(histogram)*99,'Obama wins','FontSize',14)
if analysisdate==0
    datelabel=datestr(now);
else
    datelabel=datestr(analysisdate);
end
text(202,max(histogram)*13,datelabel(1:6),'FontSize',12)
text(202,max(histogram)*7,'election.princeton.edu','FontSize',12)
if biaspct==0
    set(gcf,'PaperPositionMode','auto')
    print -djpeg EV_histogram_today.jpg
end

% Calculate median and confidence bands from cumulative histogram
confidenceintervals(3)=electoralvotes(find(cumulative_prob<=0.025,1,'last')); % 95-pct lower limit
confidenceintervals(1)=electoralvotes(find(cumulative_prob<=0.15865,1,'last')); % 1-sigma lower limit
confidenceintervals(2)=electoralvotes(find(cumulative_prob>=0.84135,1,'first')); % 1-sigma upper limit
confidenceintervals(4)=electoralvotes(find(cumulative_prob>=0.975,1,'first')); % 95-pct upper limit
probability_GOP_win=cumulative_prob(find(electoralvotes>=269,1,'first'));
modeEV(1)=find(histogram==max(histogram));
medianEV(2)=538-medianEV(1); % assume no EV go to a third candidate
modeEV(2)=538-modeEV(1); % assume no EV go to a third candidate

% Re-calculate safe EV for each party
assignedEV(1)=sum(polls.EV(find(stateprobs>=95)));
assignedEV(2)=sum(polls.EV(find(stateprobs<=5)));
assignedEV(3)=538-assignedEV(1)-assignedEV(2);

uncertain=intersect(find(stateprobs<95),find(stateprobs>5));
uncertainstates='';
for i=1:max(size(uncertain))
    uncertainstates=[uncertainstates statename(uncertain(i)) ' '];
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%% Daily file update %%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Write a file of unbiased statewise percentage probabilities
% Only write this file if bias is zero!
outputs=[medianEV modeEV assignedEV confidenceintervals totalpollsused];    
if biaspct==0
    save 'EVoutput'
%   Export probability histogram:
    dlmwrite('EV_histogram.csv',histogram')
%   Export state-by-state percentage probabilities as CSV, with 2-letter state abbreviations:
%   Each line includes hypothetical probabilities for D+2% and R+2% biases
    if exist('stateprobs.csv','file')
        delete('stateprobs.csv')
    end
    foo=(polls.margin+2)./polls.SEM;
    D2probs=round((erf(foo/sqrt(2))+1)*50);
    foo=(polls.margin-2)./polls.SEM;
    R2probs=round((erf(foo/sqrt(2))+1)*50);
    for i=1:num_states
        foo=[num2str(stateprobs(i)) ',' num2str(polls.margin(i)) ',' num2str(D2probs(i)) ',' num2str(R2probs(i)) ',' statename(i)];
        dlmwrite('stateprobs.csv',foo,'-append','delimiter','')
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%% The meta-margin %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

reality=probability_GOP_win;

if metacalc==0
    metamargin=-999;
else
    foo=biaspct;
    biaspct=round((269-medianEV(1))/1.25)/10-2;
    EV_median
    while medianEV(1) < 269
        biaspct=biaspct+.02;
        EV_median
    end
    metamargin=-biaspct;
    biaspct=foo; 
    clear foo
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%% Daily and History Update %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
outputs = [outputs metamargin];
dlmwrite('EV_estimates.csv', outputs)
if forhistory && size(polldata,2)==5
   dlmwrite('EV_estimate_history.csv',[polldata(1,5) outputs],'-append')
end
