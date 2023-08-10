import pandas as pd
import json
import matplotlib.pyplot as plt
from pandasgui import show
from typing import Union, List


class FplTweetsDataLoader:

    MAPPING = {1: 'positive',
               0: 'neutral',
               -1: 'negative'}

    def __init__(self,
                 path: str = None,
                 data: pd.DataFrame = None,
                 train: bool = True,
                 validation: bool = False,
                 test: bool = False):
        if path is None and data is None:
            raise ValueError('One of path and data should not be None!')
        if not any([train, validation, test]):
            raise ValueError('One of train, validation and test must be True!')
        self.path: Union[str, None] = path
        self.train: bool = train
        self.validation: bool = validation
        self.test: bool = test
        self.data: Union[pd.DataFrame, None] = data
        self.annotations: List = []

        self.loadData()
        self.cleanData()
        self.reformat()
        self.export()

    def loadData(self):
        if self.data is None:
            self.data = pd.read_csv(self.path)
        print(f'{self.data.shape[0]} tweets loaded!')

    def cleanData(self):
        self.data = self.data[['player', 'text', 'class']]
        self.data.drop_duplicates(['player', 'text'], inplace=True)
        # gui = show(self.data)

    def annotate(self,
                 row: pd.Series):
        return dict(sentence=row['text'],
                    aspect=row['player'],
                    sentiment=self.MAPPING[row['class']])

    def reformat(self):
        self.annotations = list(self.data.apply(lambda row: self.annotate(row), axis=1))

    def export(self):
        if self.train:
            dataset = 'train'
        elif self.validation:
            dataset = 'validation'
        else:
            dataset = 'test'
        with open(f'../data/{dataset}_tweets.json', 'w') as f:
            json.dump(self.annotations, f)



if __name__ == '__main__':
    formatter = FplTweetsDataLoader(path='../data/labelledTweets.csv')
    formatter.loadData()
    formatter.cleanData()
    formatter.reformat()
    formatter.export()