import requests
import pandas as pd
import json
from pprint import pprint


class FplData:
    def __init__(self):
        self.baseUrl ='https://fantasy.premierleague.com/api/'
        self.data = None
        self.playerNames = None
        self.positionsDict = None
        self.teams = None
        self.transfersData = None

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

    def populatePositionDict(self, response: dict) -> dict:
        playerTypes = response['element_types']  # this is a list of dictionaries
        positionDict = {}
        for type in playerTypes:
            id = type['id']
            shortName = type['singular_name_short']
            nPerSquad = type['squad_select']
            minN = type['squad_min_play']
            maxN = type['squad_max_play']
            positionDict[id] = {'name' : shortName,
                                'nPerSquad': nPerSquad,
                                'minPlaying': minN,
                                'maxPlaying': maxN}
        return positionDict

    def type2Pos(self, type: int) -> str:
        return self.positionsDict[type]['name']

    def cleanData(self, data) -> pd.DataFrame:
        if self.positionsDict is None:
            return data
        else:
            playerTypes = data.element_type.tolist()
            playerPositions = list(map(self.type2Pos, playerTypes))
            data['position'] = playerPositions
            return data

    def pullFplData(self):
        newData = self.getDataFromEndpoint()
        self.positionsDict = self.populatePositionDict(newData)
        self.data = self.dict2pandas(newData)
        self.data = self.cleanData(self.data)
        self.playerNames = self.getPlayerNamesFromPandas(self.data)

if __name__ == '__main__':
    myFpl = FplData()
    myFpl.pullFplData()

