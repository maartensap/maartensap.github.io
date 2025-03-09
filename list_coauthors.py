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


old = """Sachin Kumar
Keisuke Sakaguchi
Oren Etzioni
Regina Rini
Eunsol Choi
Franziska Roesner
Dipankar Ray
Ece Kamar
Hamid Palangi
Hanna Hajishirzi
Prithviraj Ammanabrolu
Anna Jafarpour
Eric Horvitz
James W. Pennebaker
Daniel Khashabi
Gunhee Kim
Malihe Alikhani
Pei Zhou
Youngjae Yu
Bernhard Schölkopf
Joshua B. Tenenbaum
Rada Mihalcea
Zhijing Jin
Mrinmaya Sachan
Anjalie Field
Lauren F. Klein
Melanie Walsh
Emily Allaway
Swabha Swayamdipta
Thomas Davidson
Hae Won Park
Jack Hessel
Pedro Colon-Hernandez
Sarah-Jane Leslie
Elizabeth Clark
Peter West
Chandra Bhagavatula
John Tasioulas
Kavel Rao
Nouha Dziri
Sydney Levine
Valentina Pyatkin
Vered Shwartz
Yoav Goldberg
Reza Shokri
Tadayoshi Kohno
Julia Mendelsohn
Zhicong Lu
Zixi Chen
Andrew Piper
Cathy Buerger
Cynthia Breazeal
Elliott Ash
Faeze Brahman
Michael R. Lyu
Dan Jurafsky
Max Kleiman-Weiner
Anne G. E. Collins
Jana Schaich Borg
Jena D Hwang
Joshua Garland
Katharina Reinecke
Maria Antoniak
Natalie Shapira
Ronan Le Bras
Thomas Hartvigsen
Tongshuang Wu
Xiang Ren
Yulia Tsvetkov
Hyunwoo Kim
Nanyun Peng
Saadia Gabriel
Mark Riedl
""".split("\n")

newAuthors = [a for a in allAuthors.keys() if a not in old]
embed()
