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
  if(len(i.split("Volume:"))>1):
    if(len(i.split("Issue:"))>1):
      getit=i.split("\"]");
      for j in getit:
        j=j.split("\"");
        j=j.pop();
        print j;

exit(1);
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

ids=open('ids.clump','wa');
for i in puns:
  for j in range(150):
    site="http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?asf_arn=null&asf_iid=null&asf_pun="+i+"&asf_in=null&asf_rpp=null&asf_iv=null&asf_sp=null&asf_pn="+str(j+1);
    print "plucking",i,"page",j+1;
    f = opener.open(site); s=f.read(); f.close(); 
    if(len(s.split("name=\"asf_pn\" value=\"null\""))>1): break;
    ids.write(s);


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
  author_list=[]; 
  is_journal=0; 
  pages=[0,0]; 
  bibstuff=[];
  venue='';
  keywords=[];
  year='';
  abstract=''; grab_abs=0;
  for j in s:
    if(len(j.split("meta name=\"citation_authors\""))>1):
      author_list.append(j.split("content=\"")[1].split("\">")[0]);
    elif(len(j.split("meta name=\"citation_firstpage\""))>1):
      pages[0]=j.split("content=\"")[1].split("\">")[0];
    elif(len(j.split("meta name=\"citation_lastpage\""))>1):
      pages[1]=j.split("content=\"")[1].split("\">")[0];
    elif(len(j.split("meta name=\"citation_keywords\""))>1):
      keywords=j.split("content=\"")[1].split("\">")[0].split(';');
      test=keywords.pop();
      if(len(test)): keywords.append(test);
    elif(len(j.split("meta name=\"citation_conference\""))>1):
      venue=j.split("content=\"")[1].split("\">")[0];
    elif(len(j.split("meta name=\"citation_journal_title\""))>1):
      venue=j.split("content=\"")[1].split("\">")[0];
      journal=1;
    elif(len(j.split("meta name=\"citation_"))>1):
      field=j.split("meta name=\"citation_")[1].split("\"")[0];
      value=j.split("content=\"")[1].split("\">")[0]
      bibstuff.append([field,value]);
    if(len(j.split("meta name=\"citation_date\""))>1):
      year=j.split("content=\"")[1].split("\">")[0].split().pop();

    if(grab_abs):abstract+=j;

    if(len(j.split("<a name=\"Abstract\"><h2>Abstract</h2></a>"))>1):
      grab_abs=1;
    if(len(j.split("<div class=\"body-text\">"))>1):
      grab_abs=0;

  bibtex='';
  venue=venue.replace("&amp;","and");
  if(is_journal):
    bibtex="@article{"+i+",\n journal = {"+venue+"},\n";
  else:
    bibtex="@inproceedings{"+i+",\n booktitle = {"+venue+"},\n";
  bibtex+=" author = {"; 
  first_and=0;
  for j in author_list:
    if(not first_and):
      bibtex+=j;
      first_and=1;
    else:
      bibtex+=" and "+j;
  bibtex+="},\n";
  bibtex+=" year = {"+year+"},\n";
  if(pages[0] and pages[1]):
    bibtex+=" pages = {"+str(pages[0])+'--'+str(pages[1])+"},\n";
  bibtex+=" keywords = {"
  first_and=0;
  for j in keywords:
    if(not first_and):
      bibtex+=j;
      first_and=1;
    else:
      bibtex+=", "+j;
  bibtex+="},\n";
  for j in bibstuff:
    if(not len(j[1])): continue;
    bibtex+=" "+j[0]+" = {"+j[1]+"},\n";


  abstract=abstract.replace("<p>", "");
  abstract=abstract.replace("</p>", "");
  abstract=abstract.replace("<i>", "");
  abstract=abstract.replace("<italic>", "");
  abstract=abstract.replace("</italic>", "");
  abstract=abstract.replace("<par>", "");
  abstract=abstract.replace("</par>", "");
  abstract=abstract.replace("         <span id=\"toHide", '');
  abstract=abstract.replace("\" style=\"display:none;\">", "");
  abstract=abstract.replace("<br />", "");
  abstract=abstract.replace("<span>", "");
  abstract=abstract.replace("</span>", "");
  abstract=abstract.replace("&ldquo;", "``");
  abstract=abstract.replace("&rdquo;", "\"");
  abstract=abstract.replace("&#215;", "x");
  abstract=abstract.replace("&", "\&");
  abstract=abstract.replace("%", "\%"); 
  abstract=abstract.replace("$", "\$"); 
  abstract=abstract.replace("}", ""); 
  abstract=abstract.replace("{", ""); 
  abstract=abstract.replace("<div class=\"body-text\">","")
  abstract=abstract.replace("<div>","")
  abstract=abstract.replace("</div>","")
  abstract=abstract.split();

  bibtex+=" abstract = {";
  for j in abstract: bibtex+=j+' ';
  bibtex+="},\n";
    
  bibtex+="}";
  print bibtex;
exit(1);
