import unittest
import spacy
import string

from DataEngineering.TweetFormatting import TweetFormatter

punctuation = string.punctuation


class TestUtilityFunctions(unittest.TestCase):
    def setUp(self):
        self.tweetFormatter = TweetFormatter(useSpellCheck=False, useLemma=True, removeStopWords=True)

    def test_constructor(self):
        print('---------- Testing constructor of TweetFormatter -----------------')
        self.assertFalse(self.tweetFormatter.spellCheck, 'Failed to set spellcheck')
        self.assertTrue(self.tweetFormatter.useLemmatize, 'Failed to set lemmatize')
        self.assertTrue(self.tweetFormatter.useStopWords, 'Faled to set stopwords')

    def test_setupNlp(self):
        print('---------- Testing setup of nlp -----------------')
        self.assertIsNone(self.tweetFormatter.nlp, 'nlp attribute is not None!')
        self.tweetFormatter.setupNlp()
        self.assertTrue(isinstance(self.tweetFormatter.nlp, spacy.lang.en.English), 'Failed to setup nlp')

    def test_setupStopWords(self):
        print('---------- Testing setup of stopwords -----------------')
        self.assertIsNone(self.tweetFormatter.stopwords, 'stopwords are not None')
        self.tweetFormatter.setupStopWords()
        self.assertTrue(isinstance(self.tweetFormatter.stopwords, set), 'Failed to setup stopwords')
        self.assertTrue(len(self.tweetFormatter.stopwords) > 0, 'Failed to setup stopwords')

    def test_setTweet(self):
        print('---------- Testing set tweet -----------------')
        tweet = 'This is my test tweet'
        self.assertIsNone(self.tweetFormatter.tweet, 'Tweet is not none')
        self.tweetFormatter.setTweet(tweet)
        self.assertEqual(self.tweetFormatter.tweet, tweet, 'Failed to set tweet')

    def test_getOriginalTweet(self):
        print('---------- Testing get original tweet -----------------')
        tweet = 'This is my second test tweet'
        self.tweetFormatter.setTweet(tweet)
        self.assertEqual(self.tweetFormatter.getOriginalTweet(), tweet, 'Failed to return correct tweet')

    def test_getProcessedTweetNone(self):
        """
        This test is to ensure that getProcessedTweet returns None after a new tweet has been set
        :return: void
        :rtype: void
        """
        print('---------- Testing get processed tweet after setting new tweet -----------------')
        tweet = 'This is my third test tweet'
        self.tweetFormatter.setTweet(tweet)
        self.assertIsNone(self.tweetFormatter.getProcessedTweet(), 'Processed tweet is not None even though a new tweet'
                                                                   'was just set')

    def test_checkWhiteSpace(self):
        print('---------- Testing whitespace checker -----------------')
        testOne = '     '
        testTwo = '123'
        testThree = '  1   2   3  '
        self.assertTrue(self.tweetFormatter.checkWhiteSpace(testOne), 'Failed to return True for all white space')
        self.assertFalse(self.tweetFormatter.checkWhiteSpace(testTwo), 'Failed to return False for no white space')
        self.assertFalse(self.tweetFormatter.checkWhiteSpace(testThree), 'Failed to return False for some white space')

    def test_removePunctuation(self):
        print('---------- Testing remove punctuation -----------------')
        testCases = {
            punctuation: '',
            'This tweet has no punctuation': 'This tweet has no punctuation',
            '??(This tweet has some punctuation)!!!': 'This tweet has some punctuation',
            '': '',
            ' ': ' '
        }
        for test, result in testCases.items():
            self.assertEqual(self.tweetFormatter.removePunctuation(test), result, f'Failed to correctly process {test}')

    # def test_checkSpelling(self):
    #     print('---------- Testing check spelling -----------------')
    #     self.tweetFormatter.setupNlp()
    #     testOne = 'test'
    #     testTwo = 'independnt'
    #     testThree = 'sofware'
    #     testFour = 'theraputics'
    #     self.assertEqual(self.tweetFormatter.checkSpelling(testOne), testOne,
    #                      f'Returned incorrect spelling for {testOne}')
    #     self.assertEqual(self.tweetFormatter.checkSpelling(testTwo), testTwo,
    #                      f'Returned incorrect spelling for {testTwo}')
    #     self.assertEqual(self.tweetFormatter.checkSpelling(testThree), testThree,
    #                      f'Returned incorrect spelling for {testThree}')
    #     self.assertEqual(self.tweetFormatter.checkSpelling(testFour), testFour,
    #                      f'Returned incorrect spelling for {testFour}')

    def test_lemmatize(self):
        print('---------- Testing lemmatize -----------------')
        self.tweetFormatter.setupNlp()
        testCases = {
            'running': 'run',
            'coding': 'code',
            'playing': 'play',
            'Salah': 'Salah',
            'Salah is playing football for liverpool': 'Salah be play football for liverpool'
        }
        for test, result in testCases.items():
            self.assertEqual(self.tweetFormatter.lemmatize(test), result.split(' '), f'Failed to lemmatize {test}')

    def test_removeStopWords(self):
        print('---------- Testing remove stopwords -----------------')
        self.tweetFormatter.setupStopWords()
        testCases = {
            tuple(list(self.tweetFormatter.stopwords)[:10]): (),
            tuple(['Salah', 'is', 'playing', 'football', 'for', 'liverpool']):
                tuple(['Salah', 'playing', 'football', 'liverpool']),
        }
        for test, result in testCases.items():
            r = self.tweetFormatter.removeStopWords(test)
            r = tuple(r)
            self.assertEqual(r, result, f'Failed to remove stopwords correctly for '
                                                                          f' {test}')

    def test_removeEmojis(self):
        print('---------- Testing remove emojis -----------------')
        testCases = {
            '\U0001f600 \U0001F606 \U0001F609': '  ',
            'Salah is playing football for liverpool': 'Salah is playing football for liverpool',
            '\U0001f600Salah is playing football for liverpool\U0001f600': 'Salah is playing football for liverpool'
        }
        for test, result in testCases.items():
            self.assertEqual(self.tweetFormatter.removeEmojis(test), result, f'Failed to correctly remove emojis from'
                                                                          f' {test}')

    def test_processTweet(self):
        print('---------- Testing processTweets -----------------')
        self.tweetFormatter.setupNlp()
        self.tweetFormatter.setupStopWords()
        testCases = {
            '': {'response': False, 'result': None},
            'Salah is playing football for liverpool': {'response': True,
                                                        'result': tuple(['Salah', 'play', 'football', 'liverpool'])},
            '!!!!Salah is playing football for liverpool???': {'response': True,
                                                               'result': tuple(['Salah', 'play', 'football', 'liverpool'])}
        }
        for test, result in testCases.items():
            self.tweetFormatter.setTweet(test)
            response = self.tweetFormatter.processTweet()
            self.assertEqual(response, result['response'], f'Failed to return correct response for {test}')
            if result['result'] is None:
                self.assertIsNone(self.tweetFormatter.processedTweet, f'Failed to correctly process'
                                                                          f' {test}')
            else:
                self.assertTupleEqual(tuple(self.tweetFormatter.processedTweet), result['result'],
                                      f'Failed to correctly process {test}')

    def test_removeNewLineMarkers(self):
        print('---------- Testing removeNewLineMarkers -----------------')
        testCases ={
            '\n\n\n': '   ',
            '12\n3': '12 3',
            '123': '123'
        }

        for test, result in testCases.items():
            self.assertEqual(self.tweetFormatter.removeNewLineMarkers(test), result, 'Failed to remove new line '
                                                                                     f'markers for {test}')

    def test_removeUrls(self):
        print('---------- Testing removeUrls -----------------')
        testCases ={
            'https://t.co/FAMt6HOBQg': '',
            '123  https://t.co/FAMt6HOBQg': '123  ',
            '123': '123'
        }
        for test, result in testCases.items():
            self.assertEqual(self.tweetFormatter.removeUrls(test), result, f'Failed to remove URL from {test}')

    def test_isAscii(self):
        print('---------- Testing isAscii -----------------')
        testCases = {
            '23784659hbsdygf': True,
            'hbukyf78687Ä': False,
            'Äôve': False,
            'uf8ffü§ûuf8ffüè': False
        }
        for test, result in testCases.items():
            self.assertEqual(self.tweetFormatter.isAscii(test), result, f'Failed to return correct bool for {test}')

    def test_processSpecialCharacters(self):
        print('---------- Testing processSpecialCharacters -----------------')
        testCases = {
            'This phrase is all ascii': 'This phrase is all ascii',
            'ÄÄÄ ô Äôd, ü§û': '',
            'This phrÄse has sôme ascii': 'This has ascii'
        }
        for test, result in testCases.items():
            self.assertEqual(self.tweetFormatter.processSpecialCharacters(test), result, f'Failed to process {test}')