#!/usr/bin/env python3

from parseBibtex import *
from IPython import embed
import re, os
import datetime
from glob import glob
import pandas as pd

import markdown

from collections import Counter

import pdfgen

import argparse

findPythonRE = re.compile(r"<python ([^>]+)>")
findTitleRE = re.compile(r"<title>(.+)</title>")

def includeMarkdownFile(path):
  md = open(path).read()
  return md 

def loadAndReplaceFile(fn,d="",parentPath="",silent=False):
  ffn = f"html/{d}{fn}"
  html = open(f"html/{d}{fn}").read()
  if not silent:
    print(fn)

  lastEditTime = str(datetime.date.fromtimestamp(os.path.getmtime(ffn)))
  
  for m in findPythonRE.findall(html):
    if "includeMarkdownFile" in m:
      # embed();exit()
      res = eval(m)
    else:
      res = eval(m+f"(parentPath='{parentPath}',lastEditTime=lastEditTime)")
    html= html.replace(f"<python {m}>",res)
    if not silent:
      print(fn,m)
    
  html = html.replace("lastEditTime",lastEditTime)
  html = html.replace("websiteRoot/", parentPath)
  open(f"{d}{fn}","w+").write(html)


def addHeader(**kwargs):
  return open("tools/header.html").read()

def addNavBar(parentPath="",**kwargs):
  navHTML = open("tools/nav.html").read()
  for m in findPythonRE.findall(navHTML):
    res = eval(m+f"(parentPath='{parentPath}')")
    navHTML= navHTML.replace(f"<python {m}>",res)

  return navHTML
  
def addFooter(lastEditTime="",parentPath="",**kwargs):
  html = open("tools/footer.html").read()
  # html = html.replace("lastEditTime",lastEditTime)
  # html = html.replace("websiteRoot/", parentPath)
  return html

def generatePubYearRanges(**kwargs):
  pubs = loadPubs()
  tmp = """<label class="badge year-badge btn badge-light"><input type="radio" value="{y}">{y} <small><em>({n})</em></small></label>"""
  years = [p["year"] for p in pubs]
  cntYears = Counter(years)
  allCnt = sum(cntYears.values())
  out = """<label class="badge year-badge btn badge-light active"><input type="radio" value="{y}" checked>{y} <small><em>({n})</em></small></label>""".format(y="all",n=allCnt)+"\n"
  for y, n in sorted(cntYears.items(),reverse=True):
    out += tmp.format(y=y,n=n)+"\n"
  return out

def generateTagList(**kwargs):
  pubs = loadPubs()
  tags = [t.strip() for p in pubs for t in p.get("tags","").split(",") if t]
  
  tagsCnts = Counter(tags)
  print(tagsCnts)
  
  tmp = """<label class="badge year-badge btn badge-secondary"><input type="radio" value="{y}">{y} <small><em>({n})</em></small></label>"""
  
  out = """<label class="badge year-badge btn badge-secondary active"><input type="radio" value="{y}" checked>{y} </label>""".format(y="all")+"\n"
  
  for y, n in sorted(tagsCnts.items()):
    out += tmp.format(y=y,n=n)+"\n"
  return out


def generateTagBadge(tagList):
  out = [f'<span class="badge badge-secondary">{t}</span>'
         for t in tagList]
  
  return " ".join(out)

  
def generateHTMLpublications(**kwargs):
  out = ""
  pubs = loadPubs()
  year = datetime.date.today().year+1
  for i, p in enumerate(pubs):
    type = getPubType(p)
    title = prepTitleForNonBibTex(p["title"])
    # setting the year
    if p["year"] != year:
      year = p["year"]
      out += f'<div class="row"><div class="col-12"><h4 class="year">{year}</h4></div></div>\n'

    tagList = p.get("tags","").split(",")
    tagsTxt = " ".join(tagList)
      
    out += f'<div class="row {type} {year} {tagsTxt} jumptarget" id={p["bibKey"]} style="margin-bottom: 10px;">\n'
    out += f'<div class="col-12"><h5 style="margin: 15px 0px 5px 0px">{title}</h5>\n'
    # if "neural theory-of-mind" in p["title"].lower():
    #   embed();exit()
    out += f'{p["venue"]} ({p["year"]})&nbsp;{generatePubTypeBadge(p)}&nbsp;{generateTagBadge(tagList)}<br>\n'

    out += prettifyAuthors(p)+"</div>"
    
    out += '<div class="col-12" style="font-size: .85em;"><em>Links:</em> '
    if os.path.exists("pdfs/"+p["bibKey"]+".pdf"):
      out += f'<a class="bracket-link" target="_blank" href="pdfs/{p["bibKey"]}.pdf">[pdf]</a>\n'
    if "url" in p:
      out += f'<a class="bracket-link" target="_blank" href="{p["url"]}">[url]</a>\n'
      
    # out += prettifyAuthors(p)+"<br>\n"
    # link, website, data, etc.
    if "updatedurl" in p:
      out += f'<a class="bracket-link" target="_blank" href="{p["updatedurl"]}">[updated version ({p["updateddate"]})]</a>\n'
    if "projecturl" in p:
      out += f'<a class="bracket-link" target="_blank" href="{p["projecturl"]}">[project website]</a>\n'
    if "dataurl" in p:
      out += f'<a class="bracket-link" target="_blank" href="{p["dataurl"]}">[data]</a>\n'
    if "codeurl" in p:
      out += f'<a class="bracket-link" target="_blank" href="{p["codeurl"]}">[code]</a>\n'


    # full citation link
    out += "<br><em>Citations:</em> "
    out += f'<a class="bracket-link" href="#" target="_blank" class="citation-toggle" data-toggle="collapse" data-target="#citation{i}">[full citation]</a>'
    # bibtex link
    out+= f'<a class="bracket-link" href="#" target="_blank" class="citation-toggle" data-toggle="collapse" data-target="#bibtex{i}">[bibtex]</a>'
    out+="</div>"


    
    # full citation link
    out+= f'<div class="col-12"><div id="citation{i}" class="collapse citation-box">'
    out+= fullCitation(p)
    out+= "</div>\n"
    # bibtex
    out+= f"<div id=\"bibtex{i}\" class=\"collapse bibtex citation-box\">\n"
    out+= f"<pre class=\"bibtex\">{beautifyBibtex(p)}</pre>\n"
    out+= "</div>\n"

    # news
    if "news" in p:
      out += '<span style="font-style: italic;"><strong style="color: #b88a00;">News: </strong>'
      for name, link in p["news"]:
        out += f'<a class="bracket-link" target="_blank" href="{link}">[{name}]</a>\n'
      out += "</span>"

    
    # awards
    if "awards" in p:
      out += "<span class=\"awards\">"+p["awards"]+"</span>\n"
    # accolade
    if "accolade" in p:
      out += "<span class=\"accolade\">"+p["accolade"]+"</span>\n"
    out += "</div>\n"
    out += "</div>\n"
  # embed();exit()
  return out

def generateBibtexPublications(**kwargs):
  pubs = loadPubs()
  out = ""
  for i, p in enumerate(pubs):
    # type = getPubType(p)
    
    out+= "<div>"
    out+= f"<pre>{beautifyBibtex(p)}</pre>\n"
    out+= "</div>\n"
  return out

  
def generateWordFriendlyPublications(**kwargs):
  pubs = loadPubs()
  typeToPubs = {}
  for p in pubs:
    type = getPubType(p)
    typeToPubs[type] = typeToPubs.get(type,[])
    typeToPubs[type].append(p)
    
  order = ["journal","conference","workshop","demo","other","preprint"]
  out = ""
  index = 1
  for t in order:
    out+=f'<h4 style="margin-left: 1em;">{t.title()}</h4>\n'
    out+=f'<ol start="{index}">'
    for p in typeToPubs[t]:
      # out+=f"<p><small><em>{index}.</em></small>&nbsp;"
      out+=f'<li class="pretty">'
      out+=wordCitation(p)
      # out+="</p>\n"
      out+="</li>\n"
      index += 1
    out+="</ol>"
  return out

def loadAffiliations():

  df = pd.read_csv("affiliations.csv",sep=";")
  return df.set_index("author")["affiliation"].to_dict()
  
def generateAuthors(**kwargs):
  pubs = loadPubs()
  affils = loadAffiliations()
  for p in pubs:
    p["year"] = int(p["year"])
  year = datetime.date.today().year
  nYears = 2
  
  pubsSinceN = [p for p in pubs if p["year"] >= year-nYears]
  authors = [
    [", ".join(a)
     for a in parseAuthors(p)
     if a != ["Sap", "Maarten"]]
    for p in pubsSinceN]
  from collections import Counter
  allAuthors = Counter([a for aa in authors for a in aa])
  out = "<table>"
  out += "\n".join([
    "<tr><td>"+a+"</td><td>"+ affils[a]+"</td></tr>"
    for a in allAuthors.keys() if a in affils])
  out += "</table>"
  return out


# def generateIndexFile():
#   loadAndReplaceFile("index.html")

# def generatePublicationsFile():
#   loadAndReplaceFile("publications.html")

def grabTitleOfPage(f):
  if not f.endswith("html"):
    return os.path.basename(f).replace(".", " [") +"]"
  
  m = findTitleRE.findall(open(f).read())[0]
  m = m.replace("Maarten Sap - ","").strip()
  return m

def generateNotesList(**kwargs):
  notesFiles = glob("html/notes/*.*")
  notesFiles = {os.path.basename(f):grabTitleOfPage(f)
                for f in notesFiles if "index" not in f}

  out = "<ul>\n"
  out += "\n".join([f'  <li><a href="{f}">{t}</a></li>' for f,t in notesFiles.items()])
  out +="\n</ul>\n"
  return out

def generateNotesNavBar(**kwargs):
  notesFiles = glob("html/notes/*.*")
  notesFiles = {os.path.basename(f):grabTitleOfPage(f)
                for f in notesFiles if "index" not in f}
  
  out = '<div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">\n'

  out += "\n".join([
    f'  <a class="dropdown-item" href="websiteRoot/notes/{f}">{t}</a>'
    for f,t in notesFiles.items()])
  out +="\n</div>\n"
  return out

def addBio(**kwargs):
  bio = open("bio.html").read()
  return bio

########################## news related ######################
def loadNews():
  news = [l.strip().split(",",2) for l in open("news.txt").read().split("\n")]
  news = [[datetime.datetime.strptime(d, "%m/%Y"),e,n] for d,e,n in news]
  return news  

def formatNewsItem(t):
  d,e,n = t
  n = markdown.markdown(n).replace("<p>","").replace("</p>","")
  dd = d.strftime("%B %Y")
  out = '<p style="margin-bottom: .5em;"><em><strong>'
  out+= dd+"</em></strong> "+e+":\n"
  out+= n
  out+='</p>'
  out = out.replace("<a",'<a target="_blank"')

  return out
  
def listAllNews(**kwargs):
  news = loadNews()
  out = "\n<br>\n".join(map(formatNewsItem,news))
  
  return out

def listRecentNews(**kwargs):
  news = loadNews()
  recentNews = news[:7]
  out = "\n".join(map(formatNewsItem,recentNews))
  return out
  
######################## CV related #############################

def generateFullCV(silent=False,**kwargs):
  return "CV will go here"


def generateTalksList(silent=False,**kwargs):
  data = open("cv-files/talks.md").read().strip()
  talks = data.split("\n-")

  out = '<table style="width: 100%;">'
  for tt in talks:
    out += '<tr style="border-top: 1em solid transparent;">'
    
    title, events = tt.lstrip("- ").split("\n",1)
    events = events.strip().split("\n   ")
    
    out += '<td style="width: 80%;"><strong>'+title+'</td></tr>'

    for e in events:
      date, where = e.split(" ",1)
      out += '<tr><td style="padding-left: 1em;">'+where+'</td>'
      out += '<td>'+date+'</td></tr>'
      
  out += "</table>"
  return out

def generateStudentsList(silent=False,**kwargs):
  columns = {"name": '<th width=300>Name</th>', "program": '<th style="">Program</th>',
             'startYear' : '<th style="">Dates</th>', 'endYear': '<th>end</th>', 'where' : '<th>University</th>',
             'coAdvisor': '<th width="200">Co-advisor</th>'}
  colsToDisplay = ["name","where","program","coAdvisor","startYear"]
  
  students = pd.read_csv("cv-files/students.csv")
  students["pronouns"] = '<span class="pronouns">'+students["pronouns"]+"</span>"
  students["name"] += " "+students["pronouns"]
  students["startYear"] += "&nbsp;&ndash;&nbsp;"+students["endYear"]

  students["name"] = students[["name","website"]].fillna("").apply(lambda x: ('<a href="'+x[1]+'">'+x[0]+"</a>") if x[1] else x[0], axis=1)
  
  myPhDstudents = students[students["isMyStudent"] == "yes"].fillna("")[colsToDisplay]
  
  out  = "<h3>PhD Students</h3>\n"
  
  out += myPhDstudents.to_html(index=False,escape=False,render_links=True,
                              border=0,classes="students-table",header=False)
  
  out += "\n<h3>Undergraduate &amp; Master Students</h3>\n"
  ugradsMasters = students[students["isMyStudent"] != "yes"].fillna("")[colsToDisplay]
  out += ugradsMasters.to_html(index=False,escape=False,render_links=True,
                               border=0,classes="students-table",header=False)

  columnHeader = '<thead style="text-align: left;"><tr>'+"".join([columns[c] for c in colsToDisplay])+"</tr></thead>"
  out = out.replace("<tbody>",columnHeader+"<tbody>")
  out = out.replace("<table ",'<table style="width: 100%;"')
  

  return out


# embed();exit()

#################################################################
def generateNotesFiles(silent=False):
  notesFiles = glob("html/notes/*.html")
  for ffn in notesFiles:
    fn = os.path.basename(ffn)
    loadAndReplaceFile(fn,d="notes/",parentPath="../",silent=silent)

def generateMainFiles(silent=False):
  notesFiles = glob("html/*.html")
  for ffn in notesFiles:
    fn = os.path.basename(ffn)
    loadAndReplaceFile(fn,silent=silent)
    
def generateProjectFiles(silent=False):
  projectFiles = glob("html/*/*.html")
  projectFiles = [f for f in projectFiles if "notes/" not in f]
  
  for ffn in projectFiles:
    splitPath = os.path.normpath(ffn).split(os.path.sep)
    d = os.sep.join(splitPath[1:-1])
    fn = splitPath[-1]

    loadAndReplaceFile(fn,d=d+"/",parentPath="../"*(len(splitPath)-2),silent=silent)


def generateInSubmissionList(silent=False):
  d = "pdfs/insubmission"
  if not silent:
    print(f"Generating {d}/index.html")
  fs = glob(f"{d}/*.pdf")
  fns = [os.path.basename(f) for f in fs]
  
  html = "<h1>Papers in submission</h1>\n"
  html+= '<h2 style="color: red;">do not distribute further</h2>\n'

  html+= "<ul>"+"\n".join([f'<li><a href="{f}">{f}</a></li>' for f in fns])+"</ul>"
  
  with open(os.path.join(d,"index.html"),"w+") as f:
    f.write(html)

def generateDataList(silent=False):
  if not silent:
    print("Generating data/index.html")
  d = "data/"
  fs = glob(f"{d}/*")
  fns = [os.path.basename(f) for f in fs if "index.html" not in f]
  
  html = "<h1>Various datasets</h1>\n"
  html+= '<h2 style="color: red;">do not distribute further</h2>\n'

  html+= "<ul>"+"\n".join([f'<li><a href="{f}">{f}</a></li>' for f in fns])+"</ul>"
  
  with open(os.path.join(d,"index.html"),"w+") as f:
    f.write(html)

# def generateCVpdf(silent=True):
#   if not silent:
#     print("Generating PDF version of CV")
    
#   with open("cv.html") as f:
#     pdfgen.sync.pdfgen("cv2.pdf")
  
  
if __name__ == "__main__":
  p = argparse.ArgumentParser()
  p.add_argument("-s","--silent",action="store_true")
  args = p.parse_args()
  #exit()
  generateInSubmissionList(silent=args.silent)
  generateDataList(silent=args.silent)
  
  generateNotesFiles(silent=args.silent)
  generateMainFiles(silent=args.silent)
  generateProjectFiles(silent=args.silent)


  # generateCVpdf(silent=args.silent)
