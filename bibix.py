import shelve,string,sys,os,urllib2,platform;

listdb=dict();
current_list=[];

def info():
  print "size of bib database:\t",len(main_db.keys())-1;

print "loading database...";
main_db=shelve.open('paperbank');
if(main_db.has_key('$lists')): listdb=main_db['$lists'];
else: main_db['$lists']=listdb;
info();

def save_lists():
  print "saving lists...";
  main_db['$lists']=listdb;
  main_db.sync();

def import_bib():
  if(len(prompt)<2): return;
  infile=prompt[1];
  print "loading file...";
  try:
    infile=open(infile,'r').readlines(); 
  except IOError as e:
    print "can't open"; return;
  print "parsing file..."
  cur_bib=dict(); cur_bib_info=dict(); key='0'; 
  for i in infile:
    i=string.join(string.split(i), ' '); #condense whitespace
    if(not len(i)): continue;
    i=i+'\n';
    if(i[0]=='@'):
      if(cur_bib_info!=dict()): main_db[key]=[cur_bib.copy(), cur_bib_info.copy()]; 
      cur_bib=dict(); cur_bib_info=dict(); 
      key=i.split('{')[1].split(',')[0];
      if(main_db.has_key(key)): continue;
      cur_bib_info['type']=i[1:].split('{')[0];
      cur_bib_info['citekey']=i.split('{')[1].split(',')[0];
      cur_bib_info['has_pdf']='no';
      key=i.split('{')[1].split(',')[0];
    else:
      if(len(i.split("="))>1):
        if(len(i.split(" = {")[1].split("},\n"))):
          cur_bib[i.split()[0]]=i.split(" = {")[1].split("},\n")[0];
        else:
          cur_bib[i.split()[0]]=i.split(" = {")[1].split("}\n")[0];
  main_db[key]=[cur_bib.copy(), cur_bib_info.copy()]; #last one 
  main_db.sync();
  info();

def search():
  global current_list;
  if(len(prompt)<2): return;
  querys=prompt[1:];
  results=[];
  print "searching...";
  for t,i in main_db.iteritems():
    if(t=='$lists'): continue;
    total_rank=0; all_q=1;
    for q in querys:
      rank=rank_bib(i[0],q);
      if(not rank): all_q=0; break;
      total_rank+=rank;
    if(all_q):
      results.append([total_rank,i]);
  results.sort(reverse=True);
  print len(results),"total results found!";
  current_list=results;

def rank_bib(bib,query):
  occurances=0;
  for j in bib.values():
    occurances+=j.lower().count(query.lower()); #case insenstive 
  return occurances;

def display(type):
  global current_list;
  low=0; high=len(current_list);
  if(len(prompt)>2): 
    if(is_int(prompt[1]) and is_int(prompt[2])):
      low=int(prompt[1]); high=int(prompt[2]);
  if(low>high or low<0):return;
  if(low>len(current_list)):return;
  if(high>len(current_list)): high=len(current_list);
  print ;
  for i in range(high-low):
    print "item",low+i,
    i=low+i;
    if(current_list[i][0]>0): print "- rank",current_list[i][0],
    if(type=="quick"): show_bib_quick(current_list[i][1][0]);
    else: print ;
    if(type=="short"): show_bib_summary(current_list[i][1][0]);
    if(type=="full"): show_bib_full(current_list[i][1][0]);
    if(current_list[i][1][1]['has_pdf']=='yes'): 
      print "*pdf",
      filesize=sys.getsizeof(current_list[i][1][1]['pdf_file'])/(1024);
      if(filesize<1024):
        print "("+str(filesize)+"kb)",
      else:
        print "("+str(filesize/1024)+"mb)",
    print ;
    if(type=="quick"): continue;
    extranl=0;
    for k,v in listdb.iteritems():
      for ii in v:
        if(current_list[i][1][1]['citekey']==ii): 
          print '-'+k+'-',
          extranl=1;
    if(extranl): print ;
    print ;
  if(type=="quick"): print ;

def is_int(s):
  try: 
    int(s)
    return True
  except ValueError:
    return False

def show_bib_quick(bib):
  print '-',
  if(bib.has_key('title')):
    print bib['title'],
  if(bib.has_key('series')):
    print "-",bib['series'],

def show_bib_summary(bib):
  if(bib.has_key('title')):
    print "title:",bib['title'];
  if(bib.has_key('author')):
    print "author:",bib['author'];
  if(bib.has_key('booktitle')):
    print "booktitle:",bib['booktitle'];
  elif(bib.has_key('journal')):
    print "journal:",bib['journal'];
  if(bib.has_key('year')):
    print "year:",bib['year'],
  if(bib.has_key('series')):
    print "-",bib['series'];
  else: print ;

def show_bib_full(bib):
  for k,v in bib.items():
    print k+":",v;


def download():
  global current_list;
  if(len(prompt)<3): return;
  if(not is_int(prompt[1])): return;
  entry=int(prompt[1]);
  if(entry>=len(current_list) or entry<0): return; 
  bib=current_list[entry][1][0];
  bibinfo=current_list[entry][1][1];
  opener = urllib2.build_opener()
  opener.addheaders = [('User-agent', 'Mozilla/5.0')]
  print "downloading...";
  f = opener.open(prompt[2]); pdf=f.read(); f.close();
  bibinfo['pdf_file']=pdf;
  bibinfo['has_pdf']='yes';
  main_db[bibinfo['citekey']][1]=bibinfo; 
  print "download complete";
  main_db.sync();

def acmdownload():
  global current_list;
  if(len(prompt)<2): return;
  for i in prompt[1:]:
    if(not is_int(i)): return;
    if(int(i)<0 or int(i)>=len(current_list)): return;
  for i in prompt[1:]:
    entry=int(i);
    bib=current_list[entry][1][0];
    bibinfo=current_list[entry][1][1];
    if(not bib.has_key('acmid')): print "no acmid feild";
    a_id=bib['acmid'];
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    print "downloading",str(entry)+"...";
    f = opener.open("http://portal.acm.org/ft_gateway.cfm?id="+a_id+"&type=pdf"); pdf=f.read(); f.close();
    bibinfo['pdf_file']=pdf;
    bibinfo['has_pdf']='yes';
    main_db[bibinfo['citekey']][1]=bibinfo; 
  print "download complete";
  main_db.sync();

def open_entry():
  global current_list;
  if(len(prompt)<2): return;
  if(not is_int(prompt[1])): return;
  entry=int(prompt[1]);
  if(entry>=len(current_list) or entry<0): return; 
  bibinfo=current_list[entry][1][1];
  if(bibinfo['has_pdf']!='yes'): print "no pdf"; return;
  fn='temp.pdf';
  outfile=open(fn,'wb'); outfile.write(bibinfo['pdf_file']); outfile.close(); 
  if(platform.system()=="Darwin"): os.system('open '+fn);
  else: os.system('evince '+fn);
  savin='';
  while(savin!='yes' and savin!='no'):
    savin=raw_input("--> would you like to save changes? ");
  if(savin=='yes'): 
    newpdf=open(fn,'rb').read(); 
    bibinfo['pdf_file']=newpdf;
    main_db[bibinfo['citekey']][1]=bibinfo; 
    main_db.sync();
  os.remove(fn);

def refine():
  global current_list;
  if(len(prompt)<2): return;
  querys=prompt[1:];
  results=[];
  print "refining...";
  for i in current_list:
    total_rank=0; all_q=1;
    for q in querys:
      rank=rank_bib(i[1][0],q);
      if(not rank): all_q=0; break;
      total_rank+=rank;
    if(all_q):
      results.append([total_rank,i[1]]);
  results.sort(reverse=True);
  print len(results),"total results found!";
  current_list=results;
    
def eliminate():
  global current_list;
  if(len(prompt)<3): return;
  doit='';
  while(doit!='yes' and doit!='no'):
    doit=raw_input("--> are you sure you want to do this? ");
  if(doit!='yes'): return;
  trash=[];
  for t,i in main_db.iteritems():
    if(t=='$lists'): continue;
    if(i[0].has_key(prompt[1])):
      if(i[0][prompt[1]].split()==prompt[2:]):
        trash.append(i[1]['citekey']);
  for i in trash:
    del main_db[i];
    for j in listdb.iterkeys():
      listdb[j][:] = (value for value in listdb[j] if value != i)
  print "eliminated",len(trash),"entries";
  main_db.sync();
  current_list=[];

def showlists():
  for i in listdb.iterkeys():
    print i,'-',len(listdb[i]),'entries';

def loadlist():
  global current_list;
  if(len(prompt)<2): return;
  if(not listdb.has_key(prompt[1])): return;
  current_list=[];
  for i in listdb[prompt[1]]:
    current_list.append([0,main_db[i]]);
  print "loaded",len(listdb[prompt[1]]),"entries";

def createlist():
  if(len(prompt)<2): return;
  listdb[prompt[1]]=[];
  save_lists();
  print "list created";

def deletelist():
  if(len(prompt)<2): return;
  if(not listdb.has_key(prompt[1])): return;
  doit='';
  while(doit!='yes' and doit!='no'):
    doit=raw_input("--> are you sure you want to do this? ");
  if(doit!='yes'): return;
  del listdb[prompt[1]];
  save_lists();
  print "list deleted";

def addtolist():
  global current_list;
  if(len(prompt)<3): return;
  if(not listdb.has_key(prompt[1])): return;
  for i in prompt[2:]:
    if(not is_int(i)): return;
    if(int(i)<0 or int(i)>=len(current_list)): return;
  for i in prompt[2:]:
    i=int(i);
    key=current_list[i][1][1]['citekey'];
    listdb[prompt[1]]=list(set(listdb[prompt[1]]+[key]));
  save_lists();
  print len(prompt[2:]),"entries added to list";

def removeitem():
  global current_list;
  if(len(prompt)<3): return;
  if(not listdb.has_key(prompt[1])): return;
  for i in prompt[2:]:
    if(not is_int(i)): return;
    if(int(i)<0 or int(i)>=len(current_list)): return;
  num_r=0;
  for i in prompt[2:]:
    num_r+=1;
    i=int(i);
    key=current_list[i][1][1]['citekey'];
    try:
      listdb[prompt[1]].remove(key); 
    except ValueError as e:
      num_r-=1;
  save_lists();
  print num_r,"entries removed from list";

def loadallpdfs():
  global current_list;
  current_list=[];
  for t,i in main_db.itervalues():
    if(t=='$lists'): continue;
    if(not i[1].has_key('has_pdf')): continue;
    if(i[1]['has_pdf']=="yes"):
      current_list.append([0,i]);
  print "loaded",len(current_list),"entries";

prompt=[0];

def match(inp, l):
  for i in l:
    if(inp==i): return 1;
  return 0;


while(prompt[0]!='q' and prompt[0]!='quit'):
  prompt=raw_input("--> ").split();
  if(not len(prompt)): prompt=[0];
  if(match(prompt[0],["import","i"])): import_bib();
  if(match(prompt[0],["search","s"])): search();
  if(match(prompt[0],["display","d"])): display('short');
  if(match(prompt[0],["displaybib","dbib"])): display('full');
  if(match(prompt[0],["quickdisplay","qd","ql"])): display('quick');
  if(match(prompt[0],["download","dl"])): download();
  if(match(prompt[0],["acmdownload","adl"])): acmdownload();
  if(match(prompt[0],["open","o"])): open_entry();
  if(match(prompt[0],["refine","r"])): refine();
  if(match(prompt[0],["eliminate","elim"])): eliminate();
  if(match(prompt[0],["showlists","show"])): showlists();
  if(match(prompt[0],["loadlist","load"])): loadlist();
  if(match(prompt[0],["createlist","create"])): createlist();
  if(match(prompt[0],["deletelist","del"])): deletelist();
  if(match(prompt[0],["addtolist","add"])): addtolist();
  if(match(prompt[0],["removeitem","ri"])): removeitem();
  if(match(prompt[0],["loadallpdfs","pdfs"])): loadallpdfs();
  if(match(prompt[0],["info"])): info();
  if(match(prompt[0],["help"])): showhelp();

main_db.close();