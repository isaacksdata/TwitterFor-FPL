import warnings
import csv

from TweetFormatting import TweetFormatter

warnings.filterwarnings("ignore", category=FutureWarning)


class ResponseParser:
    def __init__(self, tweetDataFileName: str, tweeterDataFileName: str):
        self.tweetDataFileName = tweetDataFileName
        self.tweeterDataFileName = tweeterDataFileName
        self.jsonResult = None
        self.Formatter = TweetFormatter()

    def parseJSONResult(self, result: tuple) -> int:
        self.jsonResult, query = result
        tweeters = self.jsonResult['includes']['users']
        tweets = self.jsonResult['data']
        self.parseTweeterData(tweeters)
        self.parseTweetData(tweets, query)
        return len(tweets)

    def parseTweetData(self, tweets: list, query: str):
        csvFile = open(self.tweetDataFileName, "a", newline="", encoding='utf-8')
        csvWriter = csv.writer(csvFile)
        for tweet in tweets:
            try:
                assert query.lower() in tweet['text'].lower()
            except AssertionError:
                pass
            else:
                metrics = tweet['public_metrics']
                nReTweets = metrics['retweet_count']
                nReplies = metrics['reply_count']
                nLikes = metrics['like_count']
                nQuotes = metrics['quote_count']
                engagement = self.getEngagement(nReTweets, nReplies, nLikes, nQuotes)
                self.Formatter.setTweet(tweet['text'])
                self.Formatter.processTweet()
                newData = [
                    tweet['author_id'],
                    tweet['id'],
                    query,
                    tweet['lang'],
                    tweet['created_at'],
                    nReTweets,
                    nReplies,
                    nLikes,
                    nQuotes,
                    engagement,
                    tweet['text']]
                csvWriter.writerow(newData)
        csvFile.close()

    def getEngagement(self, nReTweets: int, nReplies: int, nLikes: int, nQuotes: int) -> float:
        return ((nReTweets + nQuotes)*2) + (nReplies*1.5) + nLikes

    def parseTweeterData(self, tweeters: list):
        csvFile = open(self.tweeterDataFileName, "a", newline="", encoding='utf-8')
        csvWriter = csv.writer(csvFile)
        for tweeter in tweeters:
            username = tweeter['username']
            verified = tweeter['verified']
            name = tweeter['name']
            idx = tweeter['id']
            dateCreated = tweeter['created_at']
            description = tweeter['description']
            followers = tweeter['public_metrics']['followers_count']
            following = tweeter['public_metrics']['following_count']
            nTweets = tweeter['public_metrics']['tweet_count']
            newData = [
                idx,
                username,
                verified,
                name,
                dateCreated,
                followers,
                following,
                nTweets,
                self.getPopularity(followers, following),
                self.getReach(followers, nTweets),
                description]
            csvWriter.writerow(newData)
        csvFile.close()

    def getPopularity(self, nFollowers: int, nFollowing: int) -> float:
        try:
            popularity = nFollowers / nFollowing
        except ZeroDivisionError:
            popularity = nFollowers
        return popularity

    def getReach(self, nFollowers: int, nTweets: int) -> int:
        return nFollowers * nTweets
