# Data Statement for _Social Bias Inference Corpus (SBIC)_


**Dataset name**: Social Bias Inference Corpus (v2)

**Citation**: Maarten Sap, Saadia Gabriel, Lianhui Qin, Dan Jurafsky, Noah A Smith & Yejin Choi. [Social Bias Frames: Reasoning about Social and Power Implications of Language](https://homes.cs.washington.edu/~msap/pdfs/sap2020socialbiasframes.pdf). _ACL (2020)_ 

**Dataset developer**: Maarten Sap, Saadia Gabriel

**Data statement author**: Maarten Sap

## A. CURATION RATIONALE 
The main aim for this dataset is to cover a wide variety of social biases that are implied in text, both subtle and overt, and make the biases representative of real world discrimination that people experience [RWJF 2017](https://web.archive.org/web/20200620105955/https://www.rwjf.org/en/library/research/2017/10/discrimination-in-america--experiences-and-views.html). We also wanted to have some innocuous statements, to balance out biases, offensive, or harmful content.

We included online posts from the following sources:
- r/darkJokes, r/meanJokes, r/offensiveJokes
- Reddit microaggressions ([Breitfeller et al., 2019](https://www.aclweb.org/anthology/D19-1176/))
- Toxic language detection Twitter corpora ([Waseem & Hovy, 2016](https://www.aclweb.org/anthology/N16-2013/); [Davidson et al., 2017](https://www.aaai.org/ocs/index.php/ICWSM/ICWSM17/paper/viewPaper/15665); [Founa et al., 2018](https://www.aaai.org/ocs/index.php/ICWSM/ICWSM18/paper/viewPaper/17909))
- Data scraped from hate sites (Gab, Stormfront, r/incels, r/mensrights)

We wanted posts to be as self-contained as possible, therefore, we applied some filtering to prevent posts from being highly context-dependent. For Twitter data, we filter out @-replies, retweets, and links, and subsample posts such that there is a smaller correlation between AAE and offensiveness (to avoid racial bias; [Sap et al., 2019](https://www.aclweb.org/anthology/P19-1163/)). For Reddit, Gab, and Stormfront, we only select posts that are one sentence long, don't contain links, and are between 10 and 80 words. Furthemore, for Reddit, we automatically remove posts that target automated moderation. 


## B. LANGUAGE VARIETY/VARIETIES


* **BCP-47 language tag**: presumably, en-US
* **Language variety description**: predominantly white-aligned English (78%, using a lexical dialect detector, [Blodgett et al., 2016](https://www.aclweb.org/anthology/D16-1120)). We find less than 10% of posts in SBIC are detected to have the AAE dialect category.

## C. SPEAKER DEMOGRAPHIC
Due to the nature of this corpus, there is no way to know who the speakers are. But, by virtue of our data selection process, the speakers of our Reddit, Gab, and Stormfront posts are likely white men (see [Gender by subreddit](http://bburky.com/subredditgenderratios/), [Gab users](https://en.wikipedia.org/wiki/Gab_(social_network)#cite_note-insidetheright-22), [Stormfront description](https://en.wikipedia.org/wiki/Stormfront_(website))).

## D. ANNOTATOR DEMOGRAPHIC

* **Description**: Amazon mechanical turk
* **Age**: 36±10 years old
* **Gender**: 55% women, 42% men, <1% non-binary
* **Race/ethnicity** (according to locally appropriate categories): 82% White, 4% Asian, 4% Hispanic, 4% Black
* First language(s): N/A
* Training in linguistics/other relevant discipline: N/A


## E. SPEECH SITUATION


* **Description**: online on social media
* **Time**: depends on the corpus, sometime between 2014-2019
* **Place**: online
* **Modality** (spoken/signed, written): written
* **Scripted/edited vs. spontaneous**: scripted (ish, cause social media)
* **Synchronous vs. asynchronous interaction**: asynchronous
* **Intended audience**: social networks

## F. TEXT CHARACTERISTICS
Because this is a corpus of social biases, a lot of posts contain implied or overt biases against the following groups (in decreasing order of prevalence):
- gender/sexuality
- race/ethnicity
- religion/culture
- social/political
- disability body/age
- victims

## G. RECORDING QUALITY

## H. OTHER

## I. PROVENANCE APPENDIX
See paper: https://www.aclweb.org/anthology/2020.acl-main.486
## About this document

A data statement is a characterization of a dataset that provides context to allow developers and users to better understand how experimental results might generalize, how software might be appropriately deployed, and what biases might be reflected in systems built on the software.

Data Statements are from the University of Washington. Contact: [datastatements@uw.edu](mailto:datastatements@uw.edu). This document template is licensed as [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/).

This version of the markdown Data Statement is from June 4th 2020. The Data Statement template is based on worksheets distributed at the [2020 LREC workshop on Data Statements](https://sites.google.com/uw.edu/data-statements-for-nlp/), by Emily M. Bender, Batya Friedman, and Angelina McMillan-Major. Adapted to community [Markdown template](https://gist.github.com/leondz/b3a53bb807a301424e3762787a04a5da) by Leon Dercyznski.