import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import pipeline
from typing import Union


class myNLP:
    def __init__(self):
        self.model = None

    def loadModel(self, modelName: str = 'sentiment-analysis'):
        model = pipeline(modelName)
        self.model = model

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
    nlp.predict(input='This is a really mean tweet!')