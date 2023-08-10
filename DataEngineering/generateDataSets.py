import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split

from DataEngineering.FormatForTraining import FplTweetsDataLoader

seed = 100

def generateData(path: str,
                 train_prop: float = 0.7,
                 validation_prop: float = 0.2,
                 test_prop: float = 0.1):

    assert np.ceil(train_prop + validation_prop + test_prop) == 1, 'train, validation and test proportions must sum to 1'

    data = pd.read_csv(path)
    data.reset_index(inplace=True)
    N = data.shape[0]
    random.seed(seed)
    train, validation = train_test_split(data, test_size=validation_prop)
    validation, test = train_test_split(validation, test_size=test_prop)
    FplTweetsDataLoader(data=train, train=True, validation=False, test=False)
    FplTweetsDataLoader(data=validation, validation=True, train=False, test=False)
    FplTweetsDataLoader(data=test, train=False, validation=False, test=True)


if __name__ == '__main__':
    generateData('../data/labelledTweets.csv')