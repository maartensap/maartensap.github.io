#!/usr/bin/env python3

from parseBibtex import *
from IPython import embed
import re, os
import datetime
from glob import glob

findPythonRE = re.compile(r"<python ([^>]+)>")
findTitleRE = re.compile(r"<title>(.+)</title>")
def loadAndReplaceFile(fn,d="",parentPath=""):
  ffn = f"html/{d}{fn}"
  html = open(f"html/{d}{fn}").read()
  print(fn)

  lastEditTime = str(datetime.date.fromtimestamp(os.path.getmtime(ffn)))
  
  for m in findPythonRE.findall(html):
    res = eval(m+f"(parentPath='{parentPath}',lastEditTime=lastEditTime)")
    html= html.replace(f"<python {m}>",res)
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

def generateHTMLpublications(**kwargs):
  out = ""
  pubs = loadPubs()
  year = datetime.date.today().year+1
  for i, p in enumerate(pubs):
    type = getPubType(p)

    # setting the year
    if p["year"] != year:
      year = p["year"]
      out += f'<div class="row"><div class="col-12"><h4 class="year">{year}</h4></div></div>\n'
    
    out += f'<div class="row {type} jumptarget" id={p["bibKey"]} style="margin-bottom: 10px;">\n'
    out += f'<div class="col-12"><h5 style="margin: 15px 0px 5px 0px"><span class="title">{p["title"]}\n'
    if "projecturl" in p:
      out += f'</span><span class="project-url"> <a target="_blank" href="{p["projecturl"]}">[project website]</a>\n'
    out += f'</span></h5></div><div class="col-12">{p["venue"]} ({p["year"]})&nbsp;{generatePubTypeBadge(p)}</div>\n'
    out += '<div class="in-citation col-12">'
    if os.path.exists(p["bibKey"]+".pdf"):
      out += f'<a target="_blank" href="pdfs/{p["bibKey"]}.pdf">[pdf]</a>&nbsp;\n'
    if "url" in p:
      out += f'<a target="_blank" href="{p["url"]}">[url]</a>&nbsp;\n'
      
    out += prettifyAuthors(p)+"<br>\n"  
    # full citation link

    # bibtex link
    out+= f"<a href=\"#\" target=\"_blank\" class=\"citation-toggle\" data-toggle=\"collapse\" data-target=\"#bibtex{i}\">[bibtex]</a>&nbsp;"
    

    # bibtex     
    out+= f"<div id=\"bibtex{i}\" class=\"collapse bibtex citation-box\">\n"
    out+= f"<code class=\"bibtex\">{beautifyBibtex(p)}</code>\n";
    out+= "</div>\n"

    # awards
    if "awards" in p:
      out += "<br><span class=\"awards\">"+p["awards"]+"</span>\n"
    out += "</div>\n"
    out += "</div>\n"
  # embed();exit()
  return out


def generateIndexFile():
  loadAndReplaceFile("index.html")
  # html = open("html/index.html").read()
  # lastEditTime = str(datetime.date.fromtimestamp(os.path.getmtime("html/index.html")))
  # for m in findPythonRE.findall(html):
  #   res = eval(m+"(parentPath='',lastEditTime=lastEditTime)")
  #   html= html.replace(f"<python {m}>",res)

  # open("index.html","w+").write(html)
  

def generatePublicationsFile():
  loadAndReplaceFile("publications.html")
  
  # html = open("html/publications.html").read()
  # lastEditTime = str(datetime.date.fromtimestamp(os.path.getmtime("html/publications.html")))

  # for m in findPythonRE.findall(html):
  #   res = eval(m+"(parentPath='',lastEditTime=lastEditTime)")
  #   html= html.replace(f"<python {m}>",res)

  # open("publications.html","w+").write(html)

def grabTitleOfPage(f):
  if not f.endswith("html"):
    return os.path.basename(f).replace(".", " [") +"]"
  
  m = findTitleRE.findall(open(f).read())[0]
  m = m.replace("Maarten Sap - ","").strip()
  return m

def generateNotesList(**kwargs):
  print("notes list")
  notesFiles = glob("html/notes/*.*")
  notesFiles = {os.path.basename(f):grabTitleOfPage(f)
                for f in notesFiles if "index" not in f}

  out = "<ul>\n"
  out += "\n".join([f'  <li><a href="{f}">{t}</a></li>' for f,t in notesFiles.items()])
  out +="\n</ul>\n"
  return out

def generateNotesNavBar(**kwargs):
  print("notes navbar list")
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

def generateNotesFiles():
  notesFiles = glob("html/notes/*.html")
  # notesFiles = [os.path.basename(ffn) for ffn in notesFiles]
  for ffn in notesFiles:
    fn = os.path.basename(ffn)
    loadAndReplaceFile(fn,d="notes/",parentPath="../")
    
    # html = open(f"html/notes/{fn}").read()
    # print(fn)

    # lastEditTime = str(datetime.date.fromtimestamp(os.path.getmtime(ffn)))
    
    # for m in findPythonRE.findall(html):
    #   res = eval(m+"(parentPath='../',lastEditTime=lastEditTime)")
    #   html= html.replace(f"<python {m}>",res)
    #   print(fn,m)

    # open(f"notes/{fn}","w+").write(html)

def generateMainFiles():
  notesFiles = glob("html/*.html")
  # notesFiles = [os.path.basename(ffn) for ffn in notesFiles]
  for ffn in notesFiles:
    fn = os.path.basename(ffn)
    loadAndReplaceFile(fn)
  
if __name__ == "__main__":
  # generatePublicationsFile()
  # generateIndexFile()
  generateNotesFiles()
  generateMainFiles()
