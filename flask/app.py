from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import numpy as np
import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from FplApi import FplData

app = Flask(__name__)

class MyData:
    def __init__(self):
        self.twitterData = None
        self.fplData = None

    def loadTwitterData(self):
        self.twitterData = pd.read_csv('../tweet_data.csv')

    def loadFplData(self):
        self.fplData = self.getPlayerData()

    def getTwitterData(self):
        return self.twitterData

    def getFplData(self):
        return self.fplData

    def getPlayerData(self):
        myFpl = FplData()
        myFpl.pullFplData()
        return myFpl.getData()

myData = MyData()
myData.loadTwitterData()
myData.loadFplData()

@app.route('/')
def root():
    # data = pd.read_csv('../tweet_data.csv')
    # fplData = getPlayerData()
    data = myData.getTwitterData()
    fplData = myData.getFplData()
    nPlayersToShow = 20
    plotData = subsetDataByPosition(data, fplData, 'FWD')
    graphJSON = plotPlayerFrequency(plotData, nPlayersToShow)
    return render_template('plotly.html', graphJSON=graphJSON, nTweets=data.shape[0], nPlayers=nPlayersToShow)
    # return(render_template('basic.html', msg=message))


@app.route("/", methods=['POST'])
def index():
    data = myData.getTwitterData()
    fplData = myData.getFplData()
    nPlayersToShow = 20
    plotData = subsetDataByPosition(data, fplData, 'DEF')
    graphJSON = plotPlayerFrequency(plotData, nPlayersToShow)
    return render_template('plotly.html', graphJSON=graphJSON, nTweets=data.shape[0], nPlayers=nPlayersToShow)





def subsetDataByPosition(tweetData: pd.DataFrame, fplData: pd.DataFrame, position: str):
    assert position in ['GKP', 'DEF', 'MID', 'FWD']
    playerNames = fplData[fplData['position'] == position]['second_name'].tolist()
    tweetData = tweetData[tweetData['player'].isin(playerNames)]
    return tweetData

def plotPlayerFrequency(plotData: pd.DataFrame, nPlayersToShow: int):
    plotData = plotData.groupby(['player']).size().reset_index(name='counts').sort_values(by='counts',
                                                                                      ascending=False).iloc[
               :nPlayersToShow, ]

    fig = px.bar(plotData, x='player', y='counts', barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON



if __name__ == '__main__':
    root()
