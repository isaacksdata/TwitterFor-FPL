import pandas as pd
import csv
import os
import tqdm
import time
import random

from TwitterAPI import TwitterAPI
from Parser import ResponseParser
from FplApi import FplData


def setupCSVFiles(tweetFilename: str, tweeterFilename: str):
    csvFileTweet = open(tweetFilename, "a", newline="", encoding='utf-8')
    csvWriterTweet = csv.writer(csvFileTweet)
    csvWriterTweet.writerow(['authorId', 'tweetId', 'query', 'player', 'language', 'dateCreated',
                             'nReTweets', 'nReplies', 'nLikes', 'nQuotes', 'engagement',
                             'text', 'formattedText'])
    csvFileTweet.close()

    csvFileTweeter = open(tweeterFilename, "a", newline="", encoding='utf-8')
    csvWriterTweeter = csv.writer(csvFileTweeter)
    csvWriterTweeter.writerow(['authorId', 'username', 'verified', 'name', 'dateCreated',
                               'nFollowers', 'nFollowing', 'nTweets', 'popularity',
                               'reach', 'description'])
    csvFileTweeter.close()


def setupParser(tweetFilename: str, tweeterFilename: str, playerNames: list) -> ResponseParser:
    Parser = ResponseParser(tweetFilename, tweeterFilename)
    Parser.setPlayerNames(playerNames)
    return Parser


def removeDuplicates(tweetFilename: str, tweeterFilename: str):
    tweetData = pd.read_csv(tweetFilename)
    tweeterData = pd.read_csv(tweeterFilename)
    tweeterData = tweeterData.sort_values('nTweets').drop_duplicates('authorId', keep='last')
    tweetData = tweetData.sort_values('dateCreated').drop_duplicates(subset=['text', 'player'], keep='last')
    tweetData = tweetData.sort_values('engagement').drop_duplicates(subset=['text', 'player'], keep='first')
    tweeterData.to_csv(tweeterFilename, index=False)
    tweetData.to_csv(tweetFilename, index=False)


if __name__ == '__main__':
    tweetFileName = 'data/tweet_data.csv'
    tweeterFileName = 'data/tweeter_data.csv'
    if not os.path.exists(tweetFileName):
        setupCSVFiles(tweetFileName, tweeterFileName)
    myFpl = FplData()
    myFpl.pullFplData()
    players = myFpl.getPlayerNames()
    myParser = setupParser(tweetFileName, tweeterFileName, players)
    myAPI = TwitterAPI()
    tweetsCounter = 0
    myQuery = 'FPL'
    nextToken = None
    flag = True
    while flag:
        response = myAPI.makeQuery(query=myQuery, nextToken=nextToken)
        n = myParser.parseJSONResult(response)
        tweetsCounter += n
        if 'next_token' in response[0]['meta']:
            time.sleep(5)
            nextToken = response[0]['meta']['next_token']
        else:
            flag = False
            removeDuplicates(tweetFileName, tweeterFileName)
            time.sleep(5)
    print(f'Number of tweets pulled = {tweetsCounter}')
    tweetData = pd.read_csv(tweetFileName)
    validAuthorIDs = tweetData.authorId.unique().tolist()
    validAuthorIDs = list(map(str, validAuthorIDs))
    tweeterData = pd.read_csv(tweeterFileName)
    # tweeterData = tweeterData.sort_values('nTweets').drop_duplicates('authorId', keep='last')
    tweeterData = tweeterData[tweeterData['authorId'].isin(validAuthorIDs)]
    tweeterData.to_csv(tweeterFileName, index=False)
