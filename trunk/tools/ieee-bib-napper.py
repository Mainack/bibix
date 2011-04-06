#bib-napper tool, written by jason mars

import os;
import urllib2;
from urllib import FancyURLopener;

os.system("cat *.html >> snag.clump; rm *.html");

final=[];
puns=[];
f=open("snag.clump",'r').readlines();
for i in f:
  if(len(i.split("id=\"asf_pun\" name=\"asf_pun\" value=\""))>1):
    puns.append(i.split("id=\"asf_pun\" name=\"asf_pun\" value=\"")[1].split("\"/>")[0]);

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

#ids=open('ids.clump','wa');
#for i in puns:
#  for j in range(150):
#    site="http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?asf_arn=null&asf_iid=null&asf_pun="+i+"&asf_in=null&asf_rpp=null&asf_iv=null&asf_sp=null&asf_pn="+str(j+1);
#    print "plucking",i,"page",j+1;
#    f = opener.open(site); s=f.read(); f.close(); 
#    if(len(s.split("name=\"asf_pn\" value=\"null\""))>1): break;
#    ids.write(s);

#exit(1);

ars=[];
f=open("ids.clump",'r').readlines();
for i in f: 
  if(len(i.split("arnumber="))>1):
    ars=list(set(ars+[i.split("arnumber=")[1].split("\">")[0].split("\'>")[0]]));
    print len(ars);
print ars;


for i in ars:
  site="http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber="+i;
  print "plucking paper",i;
  f = opener.open(site); s=f.readlines(); f.close(); 

  
exit(1);
