function outputstring=statename(foo)

statelist=['AL AK AZ AR CA CO CT DC DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY '];
if bitand(foo>=1,foo<=51)
    ifoo=1+3*(foo-1);
    outputstring=statelist(ifoo:ifoo+1);
else
    outputstring='XX';
end
clear statelist foo ifoo
end
