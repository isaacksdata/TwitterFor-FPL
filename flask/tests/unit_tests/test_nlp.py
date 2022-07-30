import pytest
from pathlib import Path
import sys
import pandas as pd


file = Path(__file__).resolve()
parent, root = file.parent, file.parents[2]
root = str(root)
print(root)
sys.path.append(root)

from app import *
from nlp import *


def test_myNLP_constructor():
    nlp = myNLP()
    assert nlp.model is None


def test_myNLP_splitTrainTest():
    nlp = myNLP()
    data = pd.DataFrame(zip(list(range(10)),
                            list(range(10, 20)),
                            ['X', 'Y'] * 5),
                        columns=['A', 'B', 'label'])
    train, test = nlp.splitTrainTest(data=data, testProportion=0.2, labelColumn='label')
    assert train is not None
    assert test is not None
    assert train.shape[0] == 8
    assert test.shape[0] == 2

