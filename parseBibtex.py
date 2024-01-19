#!/usr/bin/env python3

from IPython import embed
import re
from urllib.parse import urlparse

entryTypeBibKeyRE = re.compile(r"@(\w+)\{(\w+),?")
titleRE = re.compile(r"title=\{([^\}]+)},?")
authorRE = re.compile(r"author=\{([^\}]+)},?")
fieldRE = re.compile(r"(\w+)=\{([^\}]+)},?")

bibtexSpecialChars = {
  "ö": r'\"{o}',
  "ä": r'\"{a}',
}
mainAuthor = "Maarten Sap"
mainAuthorFirst = "Maarten";
mainAuthorLast = "Sap";
listOfConferences = ["ACL","NAACL","EMNLP","EACL","CoNLL","AAAI","Findings of EMNLP",
                     "Findings of ACL", "Findings of NAACL", "NeurIPS","FAccT", "ICLR", "CHI"]
listOfJournals = ["Psychological Science", "Psychological Methods"]

def parseBibtex(bib):
  out = {}
  try:
    entryType, bibKey = entryTypeBibKeyRE.findall(bib)[0]
  except:
    embed();exit()
  fields = fieldRE.findall(bib)
  out = {k: v.replace("\\","") for k, v in fields}
  
  out["venue"] = out.get("journal",out.get("booktitle",""))

  out["entryType"] = entryType
  out["bibKey"] = bibKey
  if "news" in out:
    news = out["news"].strip().split(",")
    newsDomains = [n.split("/",5)[-1] if n.startswith("https://web.archive.org") else n for n in news ]
    domains = [urlparse(n).netloc.split(".",1)[1] for n in newsDomains]
    out["news"] = list(zip(domains, news))
    forMarkdown = "\n - "+"\n - ".join([f"[{d}]({u})" for d,u in out["news"]])
    # print("### ["+out["title"]+"](websiteRoot/publications.html#"+bibKey+")")
    # print(forMarkdown)
  return out


def getPubType(bibD):
  venue = bibD["venue"]
  if venue in listOfConferences:
    return "conference"
  elif "workshop" in venue.lower():
    return "workshop"
  if "journal" in bibD.keys() and bibD["journal"].lower() != "arxiv":
    return "journal"
  if "demonstration" in venue.lower() or bibD["entryType"]== "demo":
    return "demo"
  if "arxiv" in venue.lower():
    return "preprint"
  return "other"

def generatePubTypeBadge(bibD):
  pubType = getPubType(bibD)
  return f'<span class="badge badge-{pubType}">{pubType}</span>'

def parseAuthors(bibD):
  authorList = bibD["author"].split(" and ")
  authors = [a.split(", ") for a in authorList]
  return authors

def prettifyAuthors(bibD,noBold=False):
  authorList = parseAuthors(bibD)
  if "equalcontrib" in bibD.keys() and not noBold:
    ixs = bibD["equalcontrib"].split(",")
    ixs = [int(i) for i in ixs]
    for i in ixs:
      authorList[i][0] = authorList[i][0]+"<sup>*</sup>"


  try:
    out = " & ".join([fn+" "+ln for ln, fn in authorList])
  except:
    embed();exit()
  
  if len(authorList) > 1:
    out = out.replace(" & ",", ",len(authorList)-2)
  if not noBold:
    out = out.replace(mainAuthorFirst,"<strong>"+mainAuthorFirst+"</strong>")
    out = out.replace(mainAuthorLast,"<strong>"+mainAuthorLast+"</strong>")
    
  return out

def prepTitleForNonBibTex(title):
  title = title.replace("``",'"').replace("''",'"')
  return title
  
def beautifyBibtex(bibD):
  keysToSkip = ["projecturl","dataurl","equalcontrib","awards","entryType",
                "title","author","bibKey","venue","updatedurl","updateddate",
                "news", "codeurl", "accolade"]
  entryType = bibD["entryType"]
  if entryType in ["preprint", "demo"]:
    entryType = "article"
  
  out = "@"+entryType+"{"+bibD["bibKey"]+",</br>\n"
  out += "&nbsp;&nbsp;title={"+bibD["title"]+"},</br>\n"
  out += "&nbsp;&nbsp;author={"+bibD["author"]+"},</br>\n"
  for k, v in bibD.items():
    if k in keysToSkip: continue
    out += "&nbsp;&nbsp;"+k+"={"+v+"},</br>\n"
  out += "}"
  out = re.sub(r",</br>\n}","</br>\n}",out)
  for c, repl in bibtexSpecialChars.items():
    out = out.replace(c,repl)
  return out

def wordCitation(bibD):
  out = prettifyAuthors(bibD)
  out += " (" + bibD["year"] + ") "
  out += "<em>"+bibD["title"]+"</em>."

  out += f' '+bibD["venue"]
  if "volume" in bibD:
    out += " "+bibD["volume"]

  if "number" in bibD:
    out += "("+ bibD["number"] +")"
    
  out += '.'
  
  if "publisher" in bibD:
    out += " "+bibD["publisher"]+"."
  if "series" in bibD:
    out += " "+bibD["series"]+"." 
  if "pages" in bibD:
    out += " "+bibD["pages"]+"."
  
  return out.replace("  "," ").replace("  "," ").replace(". .",".")

def fullCitation(bibD):
  out = prettifyAuthors(bibD,noBold=True)
  out += " (" + bibD["year"] + ") "
  out += "<strong>"+prepTitleForNonBibTex(bibD["title"])+"</strong>."

  out += f' <em>'+bibD["venue"]
  if "volume" in bibD:
    out += " "+bibD["volume"]

  if "number" in bibD:
    out += "("+ bibD["number"] +")"
    
  out += '</em>.'
  
  if "publisher" in bibD:
    out += " "+bibD["publisher"]+"."
  if "series" in bibD:
    out += " "+bibD["series"]+"." 
  if "pages" in bibD:
    out += " "+bibD["pages"]+"."

  if "url" in bibD:
    url = bibD["url"]
    out += f' <a href="{url}">{url}</a>'
  
  return out.replace("  "," ").replace("  "," ").replace(". .",".")
  
def loadPubs():
  entries = ["@"+e.strip() for e in open("pubs.bib").read().split("\n@") if e]

  parsedEntries = [parseBibtex(e) for e in entries]
  return parsedEntries


if __name__ == "__main__":
  parsedEntries = loadPubs()
  types = {d["bibKey"]: generatePubTypeBadge(d) for d in parsedEntries}
  
  embed()
  
