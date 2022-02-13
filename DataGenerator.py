import pandas as pd
import csv
import os
import tqdm
import time

from TwitterAPI import TwitterAPI
from Parser import ResponseParser


def setupCSVFiles(tweetFilename: str, tweeterFilename: str):
    csvFileTweet = open(tweetFilename, "a", newline="", encoding='utf-8')
    csvWriterTweet = csv.writer(csvFileTweet)
    csvWriterTweet.writerow(['authorId', 'tweetId', 'query', 'language', 'dateCreated',
                             'nReTweets', 'nReplies', 'nLikes', 'nQuotes', 'engagement',
                             'text'])
    csvFileTweet.close()

    csvFileTweeter = open(tweeterFilename, "a", newline="", encoding='utf-8')
    csvWriterTweeter = csv.writer(csvFileTweeter)
    csvWriterTweeter.writerow(['authorId', 'username', 'verified', 'name', 'dateCreated',
                               'nFollowers', 'nFollowing', 'nTweets', 'description', 'popularity',
                               'reach'])
    csvFileTweeter.close()


def setupParser(tweetFilename: str, tweeterFilename: str) -> ResponseParser:
    Parser = ResponseParser(tweetFilename, tweeterFilename)
    return Parser


if __name__ == '__main__':
    tweetFileName = 'tweet_data.csv'
    tweeterFileName = 'tweeter_data.csv'
    if os.path.exists(tweetFileName):
        os.remove(tweetFileName)
    if os.path.exists(tweeterFileName):
        os.remove(tweeterFileName)
    setupCSVFiles(tweetFileName, tweeterFileName)
    myParser = setupParser(tweetFileName, tweeterFileName)
    myAPI = TwitterAPI()
    players = ['Jota', 'Salah', 'Ronaldo', 'Coutinho', 'Ramsey']
    tweetsCounter = 0
    for player in tqdm.tqdm(players):
        nextToken = None
        flag = True
        while flag:
            response = myAPI.makeQuery(query=player, nextToken=nextToken)
            n = myParser.parseJSONResult(response)
            tweetsCounter += n
            if 'next_token' in response[0]['meta']:
                time.sleep(5)
                nextToken = response[0]['meta']['next_token']
            else:
                flag = False
                time.sleep(5)
    print(f'Number of tweets pulled = {tweetsCounter}')
    # todo remove duplicate tweets by player while adding tweets
    tweetData = pd.read_csv(tweetFileName)
    tweeterData = pd.read_csv(tweeterFileName)
    tweeterData = tweeterData.sort_values('nTweets').drop_duplicates('authorId', keep='last')
    tweeterData.to_csv(tweeterFileName)
