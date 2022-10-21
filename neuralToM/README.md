# Neural ToM

Neural Theory-of-Mind? On the Limits of Social Intelligence in Large LMs

- **Social IQa**: 
  the dev examples only are at [socialIWa_v1.4_dev_wDims.jsonl](socialIWa_v1.4_dev_wDims.jsonl) 
  the full Social IQa dataset from http://maartensap.com/social-iqa/data/socialIQa_v1.4_withDims.tgz
- **ToMi**: 
  The data used on our paper, preprocessed: [ToMi-finalNeuralTOM.csv](ToMi-finalNeuralTOM.csv)
  the code to generate the stories is available at https://github.com/facebookresearch/ToMi *

*As noted in our paper, the code generates a set of story-question-answer tuples that assume an omniscient reader despite being false-belief stories (i.e., the answer is incorrect).

-----

Citation information

Our paper on neural theory of mind
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
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/D19-1598",
    doi = "10.18653/v1/D19-1598",
    pages = "5872--5877",
}
```
