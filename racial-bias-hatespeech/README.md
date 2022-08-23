# Risk of Racial Bias in Hate Speech Detection

There are three files:

## Founta dataset with dialect extracted
[`founta_all_dial.csv`](founta_all_dial.csv)


## Davidson dataset with dialect extracted
[`davidson_dial.csv`](davidson_dial.csv)


## Mturk re-annotations with no/dialect/race priming:

Collected with this [MTurk template](racialBias-dialectPriming.html),  [`sap2019risk_mTurkExperiment.csv`](sap2019risk_mTurkExperiment.csv) contains the annotations from our pilot study, with the following columns:

- annotator demographic information: annotatorAge, annotatorGender, annotatorMinority, annotatorPolitics, annotatorRace
  - since they had to enter it every time, they might not have entered the exact same data every time -- I recommend taking the most frequent value
  - note the "decline to answer" value for age was 100, so remove those when computing demographic stats!
- main questions about the offensiveness of the post: intentYN, offensive2anyoneYN, offensive2youYN
  - intent had 4 possible values, the offensiveYN questions had 3 (not counting "don't understand")
- additional race/dialect flagging: dialectIsWrong, raceIsWrong
  - simple checkbox answer to see whether workers disagreed with the dialect/race inferred by SuLin's model
- WorkerIdHashed
- text of the post: tweet
- experimental condition: condition
- condition specific text shows to users: dialect, username
- original data labels: davidson_label,founta_label


## Citations
- *Racial bias paper*:
Maarten Sap, Dallas Card, Saadia Gabriel, Yejin Choi & Noah A Smith (2019). **The Risk of Racial Bias in Hate Speech Detection.** ACL
- *Dialect extraction*:
Su Lin Blodgett, Lisa Green, and Brendan O'Connor. 2016. **Demographic dialectal variation in social media: A case study of African-American English**. In EMNLP.
- *Davidson dataset*:
Thomas Davidson, Dana Warmsley, Michael W. Macy, and Ingmar Weber. 2017. **Automated hate speech detection and the problem of offensive language**. In ICWSM.
- *Founta dataset*:
Antigoni-Maria Founta, Constantinos Djouvas, Despoina Chatzakou, Ilias Leontiadis, Jeremy Blackburn, Gianluca Stringhini, Athena Vakali, Michael Sirivianos, and Nicolas Kourtellis. 2018. **Large scale crowdsourcing and characterization of twitter abusive behavior.** In ICWSM. 

# Annotators with Attitudes

Download annotated data: [annWithAttitudes.tgz](annWithAttitudes.tgz)

Qual file: [annWithAttitudes-Qual.html](annWithAttitudes-Qual.html)

Large-scale question: [annWithAttitudes-LargeScale.html](annWithAttitudes-LargeScale.html)

## Citation

Maarten Sap, Swabha Swayamdipta, Laura Vianna, Xuhui Zhou, Yejin Choi & Noah A. Smith (2022) **Annotators with Attitudes: How Annotator Beliefs And Identities Bias Toxic Language Detection**. *NAACL*.
