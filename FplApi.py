import requests
import pandas as pd
import json
from pprint import pprint


class FplData:
    def __init__(self):
        self.baseUrl ='https://fantasy.premierleague.com/api/'
        self.data = None
        self.playerNames = None

    def setUrl(self, newUrl: str):
        self.baseUrl = newUrl

    def getUrl(self):
        return self.baseUrl

    def getData(self):
        return self.data

    def getPlayerNames(self):
        return self.playerNames

    def getDataFromEndpoint(self):
        response = requests.get(self.baseUrl+'bootstrap-static/').json()
        return response

    def dict2pandas(self, myDict: dict) -> pd.DataFrame:
        return pd.DataFrame.from_dict(myDict['elements'])

    def getPlayerNamesFromPandas(self, data: pd.DataFrame, nameColumn: str = 'web_name') -> list:
        return data[nameColumn].tolist()

    def pullFplData(self):
        newData = self.getDataFromEndpoint()
        self.data = self.dict2pandas(newData)
        self.playerNames = self.getPlayerNamesFromPandas(self.data)

