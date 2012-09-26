% Senate estimate
% Dem safe: 56 (counting Sanders and Lieberman)
% GOP safe: 38
% 6 races remain: AK, GA, KY, MN, MS_B, NC

demsafe=56;
GOPsafe=38;
un=0;
% polls newest to oldest from Pollster.com
margins_ak=[7 22 8]; % oldest 10/17-19
margins_ga=[-2 -4 -5 -9 -1 -9 -2]; % oldest 10/27
ga_lt50=[1 2 3 5]; ga_Lib=[4 5 7 0 5 0 2];
margins_ky=[-8 -7 -5 -3 -2]; % oldest 10/26-27
margins_mn=[-5 4 5 -3 -4 -6 4]; % oldest 10/24-28
margins_ms=[-7 -11 -13]; % oldest 10/20-22
margins_nc=[7 7 5 6 -1 2 9 6 3]; % oldest 10/25-26

med(1)=median(margins_ak);
med(2)=median(margins_ga);
med(3)=median(margins_ky);
med(4)=median(margins_mn);
med(5)=median(margins_ms);
med(6)=median(margins_nc);

len(1)=length(margins_ak);
len(2)=length(margins_ga);
len(3)=length(margins_ky);
len(4)=length(margins_mn);
len(5)=length(margins_ms);
len(6)=length(margins_nc);

sem(1)=mad(margins_ak)/0.6745/sqrt(length(margins_ak));
sem(2)=mad(margins_ga)/0.6745/sqrt(length(margins_ga));
sem(3)=mad(margins_ky)/0.6745/sqrt(length(margins_ky));
sem(4)=mad(margins_mn)/0.6745/sqrt(length(margins_mn));
sem(5)=mad(margins_ms)/0.6745/sqrt(length(margins_ms));
sem(6)=mad(margins_nc)/0.6745/sqrt(length(margins_nc));

alldists=zeros(1,7);num=0;allprobs=zeros(1,6);
for diff=-2:0.2:2;
    
for i=1:6
       z(i)=(med(i)+diff)/max(sqrt(sem(i)*sem(i)+un*un),sqrt(1/500/len(i)));
end


senate_probs=tcdf(z,len);

%Georgia
% these lines are equivalent to the assumption that undecideds can break up
% to 30-70 in either direction, uniformly distributed.
p_flip=(margins_ga(ga_lt50) + diff + 0.4*ga_Lib(ga_lt50)) ./ ga_Lib(ga_lt50)/0.8;
for i=1:length(p_flip)
   p_flip(i) = min(p_flip(i),1);
   p_flip(i) = max(p_flip(i),0);
end
senate_probs(2)=senate_probs(2)*(length(margins_ga)-length(ga_lt50))/length(margins_ga)+median(p_flip)*length(ga_lt50)/length(margins_ga);

[diff sum(senate_probs)];

senate_dist=[1-senate_probs(1) senate_probs(1)];
for i=2:6
    senate_dist=conv(senate_dist,[1-senate_probs(i) senate_probs(i)]);
end

allprobs=allprobs+senate_probs;
alldists=alldists+senate_dist;
num=num+1;
end
alldists=alldists/num;
allprobs=allprobs/num;
alldists=alldists*100;
bar(56:62,alldists)
grid on
xlabel('Democratic/Independent Senate seats')
ylabel('Probability (%)')

dlmwrite('Sen_histogram.csv', alldists');

mode_dem=demsafe-1+find(alldists==max(alldists));
mode_gop=100-mode_dem;
prob_60seats=sum(alldists(5:7));

dlmwrite('Sen_estimates.csv', [mode_dem mode_gop prob_60seats]);
