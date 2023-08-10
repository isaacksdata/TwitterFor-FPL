import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import pipeline
from typing import Union
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request

model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
irony_model_path = "cardiffnlp/twitter-roberta-base-irony"



class myNLP:
    def __init__(self):
        self.model = None
        self.ironyModel = None
        self.irony_tokenizer = None
        self.irony_labels = []

    def loadModel(self, modelName: str = 'sentiment-analysis'):
        model = pipeline(modelName, model=model_path, tokenizer=model_path)
        self.model = model

    def loadIronyModel(self):
        self.irony_tokenizer = AutoTokenizer.from_pretrained(irony_model_path)

        # download label mapping
        mapping_link = "https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/irony/mapping.txt"
        with urllib.request.urlopen(mapping_link) as f:
            html = f.read().decode('utf-8').split("\n")
            csvreader = csv.reader(html, delimiter='\t')
        self.irony_labels = [row[1] for row in csvreader if len(row) > 1]

        # PT
        self.ironyModel = AutoModelForSequenceClassification.from_pretrained(irony_model_path)
        # model.save_pretrained(irony_model_path)

    def predict_irony(self,
                      input: str):
        encoded_input = self.irony_tokenizer(input, return_tensors='pt')
        output = self.ironyModel(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        return self.ironyScoresToLabel(scores)

    def ironyScoresToLabel(self, scores):
        i = np.argmax(scores)
        l = self.irony_labels[i]
        return l, scores[i]

    def predict(self, input: Union[str, list]) -> list:
        if not isinstance(input, list) and isinstance(input, str):
            input = [input]
            y = self.model(input)
            return y
        elif isinstance(input, list):
            y = self.model(input)
            return y
        else:
            return None

    @staticmethod
    def splitTrainTest(data: pd.DataFrame, testProportion: float = 0.2, labelColumn: str = None) -> tuple:
        """
        Take an input dataset and randomly assign rows to train and test according to the train proportion value.
        Values in labelColumn are split evenly across train and test.
        :param data: the input dataframe
        :type data: pd.DataFrame
        :param testProportion: the proportion of rows to assign to test
        :type testProportion: float
        :param labelColumn: column to stratify split on
        :type labelColumn: str
        :return: train, test
        :rtype: (pd.DataFrame, pd.DataFrame)
        """
        y = data.pop(labelColumn).to_frame()
        X = data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, stratify=y, test_size=testProportion)
        train = pd.concat([X_train, y_train], axis=1)
        test = pd.concat([X_test, y_test], axis=1)
        return train, test

if __name__ == '__main__':
    nlp = myNLP()
    nlp.loadModel()
    nlp.loadIronyModel()
    nlp.predict(input='This is a really mean tweet!')
    l, s = nlp.predict_irony(input='I feel like a million bucks.')
    print(f'{l} : {s}')