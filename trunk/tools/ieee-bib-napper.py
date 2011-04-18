#bib-napper tool, written by jason mars

import os;
import urllib2;
from urllib import FancyURLopener;

ars=open("aid.list","r").read().split('\n');

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

master=open("master.bib",'w');

for i in ars:
  site="http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber="+i;
  print "plucking paper",i;
  f = opener.open(site); s=f.readlines(); f.close(); 
  author_list=[]; 
  is_journal=0; 
  pages=[0,0]; 
  bibstuff=[];
  venue='';
  year='';
  abstract=''; grab_abs=0; multiline=0; mlfield=""; mlvalue="";
  for j in s:
    if(len(j.split("meta name=\"citation_authors\""))>1):
      author_list.append(j.split("content=\"")[1].split("\">")[0]);
    elif(len(j.split("meta name=\"citation_firstpage\""))>1):
      pages[0]=j.split("content=\"")[1].split("\">")[0];
    elif(len(j.split("meta name=\"citation_lastpage\""))>1):
      pages[1]=j.split("content=\"")[1].split("\">")[0];
    elif(len(j.split("meta name=\"citation_conference\""))>1):
      venue=j.split("content=\"")[1].split("\">")[0];
    elif(len(j.split("meta name=\"citation_journal_title\""))>1):
      venue=j.split("content=\"")[1].split("\">")[0];
      journal=1;
    elif(multiline or len(j.split("meta name=\"citation_"))>1):
      if(not multiline):
        field=j.split("meta name=\"citation_")[1].split("\"")[0];
        value=j.split("content=\"")[1].split("\">")[0]
        if(len(j.split("content=\"")[1].split("\">"))<2):
          multiline=1; mlvalue=value; mlfield=field;
        else: bibstuff.append([field,value]);
      elif(multiline):
        if(len(j.split("\">"))>1):
          mlvalue+=j.split("\">")[0]; mlvalue=mlvalue.replace("\n"," ");
          bibstuff.append([mlfield,mlvalue]); multiline=0;
        else:
          mlvalue+=j; 
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
  for j in bibstuff:
    if(not len(j[1])): continue;
    if(j[0]=="keywords"): j[1]=j[1].replace(";",", ");
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
  if(bibtex.find("title")==-1): printf("You've been blocked!"); exit(1);
  bibtex=bibtex.replace("&#039;", "'");
  print bibtex;
  master.write(bibtex+'\n\n');
master.close();
