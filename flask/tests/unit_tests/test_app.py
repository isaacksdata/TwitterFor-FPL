import pytest
from pathlib import Path
import sys
import pandas as pd


file = Path(__file__).resolve()
parent, root = file.parent, file.parents[2]
sys.path.append(str(root))

from app import *


def test_myData_constructor():
    data = MyData()
    assert data.twitterData is None
    assert data.fplData is None


def test_myData_getTwitterData():
    data = MyData()
    twitterData = data.getTwitterData()
    if data.twitterData is None:
        assert twitterData is None
    elif isinstance(data.twitterData, pd.DataFrame):
        assert isinstance(twitterData, pd.DataFrame)
        assert twitterData.shape == data.twitterData.shape


def test_myData_loadTwitterData():
    data = MyData()
    data.loadTwitterData(directory='/Users/isaackitchen-smith/PycharmProjects/FPLTwitterScraper')
    assert data.twitterData is not None
    assert isinstance(data.twitterData, pd.DataFrame)
    assert 'class' in data.twitterData.columns



