# Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs

This page contains the preprocessed data for our EMNLP 2022 paper on Neural Theory of Mind.

### Social IQa

The dev examples only are at [socialIWa_v1.4_dev_wDims.jsonl](socialIWa_v1.4_dev_wDims.jsonl). Relevant fields in each line:

- `context`, `question`, `answerA`, `answerB`, `answerC`: self-explanatory.
- `label_letter`,`label_ix`: correct answer letter and index (A: 0, B: 1, C: 2)
- `promptQuestionFocusChar`: either protagonist (x) or others (o); whether the question is asking about the protagonist / main character of the situation, or others involved. This is automatically extracted from the promptDim reasoning dimension, so may not be 100% accurate since SocialIQa workers might have re-focused the question (tho that is not so often a problem from manual inspection).
- `reasoningDim`: reasoning dimension regardless of focus character
- `promptDim`: reasoning dimension + focus character: ATOMIC 2019 dimension that was used to prompt the question. See Table 3 in the Appendix of our paper for dimension explanations.

Note, the full Social IQa dataset from [http://maartensap.com/social-iqa/data/socialIQa_v1.4_withDims.tgz](http://maartensap.com/social-iqa/data/socialIQa_v1.4_withDims.tgz).

### ToMi

The data used on our paper, preprocessed: [ToMi-finalNeuralTOM.csv](ToMi-finalNeuralTOM.csv): The relevant columns are:

- `story`, `question`, `answer`:  self-explanatory
- `cands`, `answerMem`, `answerReal`: both answer candidates, along with the original location (answerMem) and the final location of the object (answerReal)
- `factVsMind` : either *fact* or *mind*, describes whether the question is factual one (memory or reality) or about beliefs (first or second order)
- `qOrder`: reasoning order is one of *reality*, *memory*, *first_order*, *second_order*
- `falseTrueBelief`: either *false* or *true*; whether reasoning about false beliefs is needed to answer the question (i.e., whether someone was out of the room when the object was moved)

The code to generate the stories is available at [https://github.com/facebookresearch/ToMi](https://github.com/facebookresearch/ToMi) . 
IMPORTANT: as noted in our paper, the code generates a set of story-question-answer tuples that assume an omniscient reader despite being false-belief stories (i.e., the answer is incorrect).

-----

### Citation information

Our paper on Neural Theory of Mind:
```bibtex
@inproceedings{sap2022neuralToM,
  title={Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs},
  author={Sap, Maarten and LeBras, Ronan and Fried, Daniel and Choi, Yejin},
  year={2022},
  journal={EMNLP}
}
```

The Social IQa paper:
```bibtex
@inproceedings{sap2019socialIQa,
  title={Social IQa: Commonsense Reasoning about Social Interactions},
  author={Sap, Maarten and Rashkin, Hannah, and Chen, Derek and LeBras, Ronan and Choi, Yejin},
  year={2019},
  booktitle={EMNLP},
  url={https://www.aclweb.org/anthology/D19-1454}
}
```

The ToMi paper:
```bibtex
@inproceedings{le-etal-2019-revisiting,
    title = "Revisiting the Evaluation of Theory of Mind through Question Answering",
    author = "Le, Matthew  and
      Boureau, Y-Lan  and
      Nickel, Maximilian",
    booktitle = "EMNLP-IJCNLP",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/D19-1598",
    doi = "10.18653/v1/D19-1598",
    pages = "5872--5877",
}
```
