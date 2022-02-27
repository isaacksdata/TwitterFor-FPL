"""
This script contains functionality to format tweets ready for deep NLP solutions
"""
import spacy
import string
import re
import contextualSpellCheck


punctuation = string.punctuation


class TweetFormatter:
    def __init__(self, useSpellCheck: bool = False, useLemma: bool = True, removeStopWords: bool = True):
        self.tweet = None
        self.processedTweet = None
        self.spellCheck = useSpellCheck
        self.useLemmatize = useLemma
        self.useStopWords = removeStopWords
        self.nlp = None
        self.stopwords = None

    def setupNlp(self):
        self.nlp = spacy.load('en_core_web_sm')
        contextualSpellCheck.add_to_pipe(self.nlp)

    def setupStopWords(self):
        self.stopwords = spacy.lang.en.stop_words.STOP_WORDS

    def setTweet(self, text: str):
        self.tweet = text
        if self.processedTweet is not None:
            self.processedTweet = None

    def getOriginalTweet(self) -> str:
        return self.tweet

    def getProcessedTweet(self) -> list:
        return self.processedTweet

    def processTweet(self) -> bool:
        if self.tweet is not None:
            if not self.checkWhiteSpace(self.tweet) and self.tweet != '':
                self.processedTweet = self.removePunctuation(self.tweet)
                self.processedTweet = self.removeEmojis(self.processedTweet)
                if self.spellCheck:
                    self.processedTweet = self.checkSpelling(self.processedTweet)
                if self.useLemmatize:
                    self.processedTweet = self.lemmatize(self.processedTweet)
                if self.useStopWords:
                    self.processedTweet = self.removeStopWords(self.processedTweet)
                return True
            else:
                return False
        else:
            return False

    def removePunctuation(self, text: str) -> str:
        for i in punctuation:
            text = text.replace(i, '')
        return text

    def checkWhiteSpace(self, text: str) -> bool:
        return text.isspace()

    def checkSpelling(self, text: str) -> str:
        doc = self.nlp(text)
        text = doc._.outcome_spellCheck
        return text

    def lemmatize(self, text: str) -> str:
        doc = self.nlp(text)
        lemmatized_output = [token.lemma_ for token in doc]
        return lemmatized_output

    def removeStopWords(self, tokens: list) -> list:
        tokens = [token for token in tokens if token not in self.stopwords]
        return tokens

    def removeEmojis(self, text: str) -> str:
        regrex_pattern = re.compile(pattern="["
                                            u"\U0001F600-\U0001F64F"  # emoticons
                                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                            "]+", flags=re.UNICODE)
        return regrex_pattern.sub(r'', text)

