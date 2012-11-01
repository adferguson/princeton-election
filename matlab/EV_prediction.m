% The first three lines need to be removed, and replaced by passing the % Meta-Margin and today's date to the script.

MM=metamargin; % today's Meta-Margin

today=floor(now)
N=datenum(2012,11,6)-today; % assuming date is set correctly in machine
% MMdrift=min(0.4*sqrt(N),1.8) % random-walk drift as seen empirically
MMdrift=min(sqrt(0.4*0.4*N+0.25),1.8) % the 0.25 term adds a minimal uncertainty
MMdrift=max(MMdrift,0.2) % just in case something is screwy with date

% cover range of +/-4 sigma
Mrange=[MM-4*MMdrift:0.02:MM+4*MMdrift];

% What is near-term drift starting from conditions now?
now=tpdf((Mrange-MM)/MMdrift,3); % long-tailed distribution. you never know.
now=now/sum(now);

% What was long-term prediction? (the prior)
M2012=3.26; M2012SD=2.2; % parameters of long-term prediction
prior=tpdf((Mrange-M2012)/M2012SD,1); %make it really long-tailed, df=1
prior=prior/sum(prior);

% Combine to make prediction
pred=now.*prior; % All hail Reverend Bayes
pred=pred/sum(pred);


plot(Mrange,now,'-k') % drift from today
hold on
plot(Mrange,prior,'-g') % the prior
plot(Mrange,pred,'-r') % the prediction
grid on

% Define mean and error bands for prediction
predictmean=sum(pred.*Mrange)/sum(pred)
for i=1:length(Mrange)
   cumulpredict(i)=sum(pred(1:i));
end
Msig1lo=Mrange(min(find(cumulpredict>normcdf(-1,0,1))))
Msig1hi=Mrange(min(find(cumulpredict>normcdf(+1,0,1))))
Msig2lo=Mrange(min(find(cumulpredict>normcdf(-2,0,1))))
Msig2hi=Mrange(min(find(cumulpredict>normcdf(+2,0,1))))

% Now convert to EV using data from mid-August and some added points at the
% ends. If the race swings far, these endpoints need to be re-evaluated.
mmf=[-1.48 -.74 0 .74 1.4800 1.8125 2.1383 2.5667 3.3200 3.7400 4.2000 4.6600 5.1050 6 7 8 9 10 11 12];
evf=[247 258 269 280 290.0000 299.2500 304.1667 310.0000 321.6667 328  343 347 347 347 347 347 347 358 369 383];
bands = interp1(mmf,evf,[predictmean Msig1lo Msig1hi Msig2lo Msig2hi],'spline');
bands = round(bands)
ev_prediction = bands(1);
ev_1sig_low = bands(2);
ev_1sig_hi = bands(3);
ev_2sig_lo = bands(4);
ev_2sig_hi = bands(5);

bayesian_winprob=sum(pred(find(Mrange>=0)))/sum(pred)
drift_winprob=tcdf(MM/MMdrift,3)

%% write to csv for plotter scripts
outputs = [ ev_1sig_low ev_1sig_hi ev_2sig_lo ev_2sig_hi ];
dlmwrite('EV_prediction.csv', outputs)

%% write probabilitiess to csv
outputs = [ bayesian_winprob drift_winprob ];
dlmwrite('EV_prediction_probs.csv', outputs)

%% write meta-margin prediction to csv for plotter scripts
outputs = [ Msig1lo Msig1hi Msig2lo Msig2hi ];
dlmwrite('EV_prediction_MM.csv', outputs)
