clear
close
load EV_estimate_history.csv
%    Each line of EV_estimate_history should contain:
%    1 value - date code
%    2 values - medianEV for the two candidates, where a margin>0 favors the first candidate (in our case, Obama);
%    2 values - modeEV for the two candidates;
%    3 values - assigned (>95% prob) EV for each candidate, with a third entry for undecided;
%    4 values - confidence intervals for candidate 1's EV: +/-1 sigma, then
%    95% band; and
%    1 value - number of state polls used to make the estimates.
%    1 value - (calculated by EV_metamargin and appended) the meta-margin.

[dates,ix]=sort(EV_estimate_history(:,1));
medianBO=EV_estimate_history(ix,2);
modeBO=EV_estimate_history(ix,4);
lowBO95=EV_estimate_history(ix,11);
highBO95=EV_estimate_history(ix,12);

phandle=plot([0 365],[269 269],'r-','LineWidth',1);
hold on
monthticks=datenum(0,4:12,1);
set(gca,'xtick',monthticks)
set(gca,'ytick',[160:20:380])
set(gca,'XTickLabel',{'              Apr','              May','              Jun','              Jul','              Aug','              Sep','              Oct','         Nov'})
grid on
axis([90 320 160 380])
set(gcf, 'InvertHardCopy', 'off');
title('Median EV estimator with 95% confidence interval','FontSize',14)
ylabel('Obama EV','FontSize',14)
text(95,172,'election.princeton.edu','FontSize',14)

plot(dates,medianBO,'-k','LineWidth',1.5)
[fillhandle,msg]=jbfill(dates',highBO95',lowBO95','k','w',1,0.2);
% see http://www.mathworks.com/matlabcentral/fileexchange/loadFile.do?objectId=13188&objectType=FILE

% still could add:
% right hand axis labels for McCain EV
% text(330,285,'McCain EV','Rotation',270,'HorizontalAlignment','center','VerticalAlignment','middle','FontSize',14)

set(gcf,'PaperPositionMode','auto')
print -djpeg EV_history.jpg
