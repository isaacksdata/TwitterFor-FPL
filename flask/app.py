from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import sys
from pathlib import Path
import random


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
        if 'class' not in self.twitterData.columns:
            self.twitterData['class'] = -1

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

    def getTweet(self):
        data = self.getTwitterData()
        idx = random.choice(list(range(data.shape[0])))
        tweet = data.loc[idx, 'text']
        formattedTweet = data.loc[idx, 'formattedText']
        tweetId = data.loc[idx, 'tweetId']
        player = data.loc[idx, 'player']
        return tweet, formattedTweet, tweetId, player

    def updateTweetClassification(self, tweetId: int, label: int):
        idx = self.twitterData[self.twitterData['tweetId'] == tweetId].index.tolist()[0]
        self.twitterData.loc[idx, 'class'] = label

    def onSaveTwitterData(self):
        try:
            self.twitterData.to_csv('../tweet_data.csv')
        except Exception:
            return False
        else:
            return True


class myConfig:
    def __init__(self):
        self.nPlayers = 20
        self.position = 'MID'
        self.tweetId = None

    def setNPlayers(self, value: int):
        self.nPlayers = value

    def setPosition(self, newPos: str):
        self.position = newPos

    def getNPlayers(self):
        return self.nPlayers

    def getPosition(self):
        return self.position

    def setTweetId(self, id: int):
        self.tweetId = id

    def getTweetId(self):
        return self.tweetId


myData = MyData()
myData.loadTwitterData()
myData.loadFplData()
cfg = myConfig()


def replotPlayerFrequency(cfg):
    data = myData.getTwitterData()
    fplData = myData.getFplData()
    graphJSON = plotSubplots(data, fplData,  cfg.getNPlayers(), cfg.getPosition())

    return render_template('plotly.html', graphJSON=graphJSON, nTweets=data.shape[0], nPlayers=cfg.getNPlayers())


@app.route('/')
def root():
    return replotPlayerFrequency(cfg)

@app.route('/submitClassification', methods=['POST'])
def onClassification():
    tweetId = cfg.getTweetId()
    assert tweetId is not None
    submittedClass = request.form['classify_button']
    if submittedClass == 'Positive':
        label = 1
    elif submittedClass == 'Negative':
        label = 0
    else:
        label = -1
    myData.updateTweetClassification(tweetId, label)
    return onClassify()


@app.route('/saveTwitterData', methods=['POST'])
def onSaveTwitterData():
    response = myData.onSaveTwitterData()
    assert response
    return replotPlayerFrequency(cfg)


@app.route('/returnToPlots', methods=['POST'])
def showPlots():
    if request.method == 'POST':
        return replotPlayerFrequency(cfg)
    else:
        pass


@app.route("/newPosition", methods=['POST'])
def index():
    if request.method == 'POST':
        pos = request.form['position_button']
        cfg.setPosition(pos)
        return replotPlayerFrequency(cfg)
    else:
        print('No GET method is enabled')


@app.route("/classifyTweets", methods=['POST'])
def onClassify():
    tweet, formattedTweet, tweetId, player = myData.getTweet()
    cfg.setTweetId(tweetId)
    return render_template('classify.html', tweet=tweet, player=player, formattedTweet=formattedTweet)


@app.route('/nPlayers', methods=['POST'])
def changeNumberOfPlayers():
    nPlayers = int(request.form['nPlayers'])
    cfg.setNPlayers(nPlayers)
    return replotPlayerFrequency(cfg)


def subsetDataByPosition(tweetData: pd.DataFrame, fplData: pd.DataFrame, position: str):
    assert position in ['GKP', 'DEF', 'MID', 'FWD']
    playerNames = fplData[fplData['position'] == position]['second_name'].tolist()
    tweetData = tweetData[tweetData['player'].isin(playerNames)]
    return tweetData


# def plotPlayerFrequency(plotData: pd.DataFrame, nPlayersToShow: int):
#     plotData = plotData.groupby(['player']).size().reset_index(name='counts').sort_values(by='counts',
#                                                                                       ascending=False).iloc[
#                :nPlayersToShow, ]
#
#     fig = px.bar(plotData, x='player', y='counts', barmode='group')
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON
#
#
# def plotSentiment(plotData: pd.DataFrame):
#     plotData = plotData.groupby(['class']).size().reset_index(name='counts')
#     fig = px.bar(plotData, x='class', y='counts', barmode='group')
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON


def plotSubplots(data: pd.DataFrame, fplData: pd.DataFrame,  nPlayers: int, position: str):
    playerData = subsetDataByPosition(data, fplData, position)
    playerData = playerData.groupby(['player']).size().reset_index(name='counts').sort_values(by='counts',
                                                                                      ascending=False).iloc[
               :nPlayers, ]
    sentData = data.groupby(['class']).size().reset_index(name='counts')
    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(
        go.Bar(x=playerData['player'], y=playerData['counts']),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=list(map(str, sentData['class'].tolist())), y=sentData['counts']),
        row=2, col=1
    )

    fig.update_layout(height=600, width=800, title_text="Side By Side Subplots")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


if __name__ == '__main__':
    app.run()
