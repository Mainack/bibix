#bib-napper tool, written by jason mars

import os;
import urllib2;
from urllib import FancyURLopener;

os.system("cat *.html >> snag.clump; rm *.html");

final=[];
puns=[];
jpuns=[];
f=open("snag.clump",'r').readlines();
for i in f:
  if(len(i.split("id=\"asf_pun\" name=\"asf_pun\" value=\""))>1):
    value = i.split("id=\"asf_pun\" name=\"asf_pun\" value=\"")[1].split("\"/>")[0];
    if(value!="null"):
      puns.append(i.split("id=\"asf_pun\" name=\"asf_pun\" value=\"")[1].split("\"/>")[0]);
  if(len(i.split("Volume:"))>1):
    if(len(i.split("Issue:"))>1):
      getit=i.split("\"]");
      for j in getit:
        j=j.split("\"");
        if(len(j)>1):
          jpuns.append(j.pop());

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

ids=open('ids.clump','wa');
for i in puns:
  for j in range(150):
    site="http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?asf_arn=null&asf_iid=null&asf_pun="+i+"&asf_in=null&asf_rpp=null&asf_iv=null&asf_sp=null&asf_pn="+str(j+1);
    print "plucking",i,"conference page",j+1;
    f = opener.open(site); s=f.read(); f.close(); 
    if(len(s.split("name=\"asf_pn\" value=\"null\""))>1): break;
    ids.write(s);
for i in jpuns:
  for j in range(150):
    site="http://ieeexplore.ieee.org/xpl/tocresult.jsp?asf_arn=null&asf_iid="+i+"&asf_pun=null&asf_in=null&asf_rpp=null&asf_iv=null&asf_sp=null&asf_pn="+str(j+1);
    print "plucking",i,"journal page",j+1;
    f = opener.open(site); s=f.read(); f.close(); 
    if(len(s.split("<strong>No articles found</strong>"))>1): break;
    ids.write(s);


ars=[];
f=open("ids.clump",'r').readlines();
for i in f: 
  if(len(i.split("arnumber="))>1):
    ars=list(set(ars+[i.split("arnumber=")[1].split("\">")[0].split("\'>")[0]]));
aid=open('aid.list', 'w');
for i in ars:
  aid.write(i+'\n');
