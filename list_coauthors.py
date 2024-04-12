# IPython log file
from IPython import embed
from collections import Counter
from parseBibtex import *
ps = loadPubs()
authors = [parseAuthors(b,reverse_order=True) for b in ps
           if int(b["year"]) > 2021 and "queer" not in b["title"].lower()]
authorNames = [[" ".join(a) for a in auths] for auths in authors]

allAuthors = Counter([a for auths in authorNames for a in auths])

print("\n".join(allAuthors.keys()))
# embed()
