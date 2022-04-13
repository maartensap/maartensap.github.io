#!/usr/bin/env python3

from parseBibtex import *
from IPython import embed
import re, os
import datetime

findPythonRE = re.compile(r"<python ([^>]+)>")

def addHeader():
  return open("tools/header.html").read()

def addNavBar():
  return open("tools/nav.html").read()

def addFooter():
  return open("tools/footer.html").read()

def generateHTMLpublications():
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

  

def generatePublicationsFile():
  html = open("html/publications.html").read()
  for m in findPythonRE.findall(html):
    res = eval(m+"()")
    html= html.replace(f"<python {m}>",res)

  open("publications.html","w+").write(html)
  

if __name__ == "__main__":
  generatePublicationsFile()

  
