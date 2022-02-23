"""
This script contains functionality to format tweets ready for deep NLP solutions
"""
import spacy
import string
import re
import contextualSpellCheck


punctuation = string.punctuation


class TweetFormatter:
    def __init__(self, useSpellCheck: bool = False, useLemma: bool = True):
        self.tweet = None
        self.spellCheck = useSpellCheck
        self.useLemmatize = useLemma
        self.nlp = spacy.load('en_core_web_sm')
        contextualSpellCheck.add_to_pipe(self.nlp)

    def setTweet(self, text: str):
        self.tweet = text

    def processTweet(self):
        if self.tweet is not None:
            text = self.removePunctuation(self.tweet)
            if self.spellCheck:
                text = self.checkSpelling(text)
            if self.useLemmatize:
                text = self.lemmatize(text)

    def removePunctuation(self, text: str) -> str:
        for i in punctuation:
            text = text.replace(i, '')
        text = self.removeEmojis(text)
        return text

    def checkSpelling(self, text: str) -> str:
        doc = self.nlp(text)
        text = doc._.outcome_spellCheck
        return text

    def lemmatize(self, text: str) -> str:
        doc = self.nlp(text)
        lemmatized_output = " ".join([token.lemma_ for token in doc])
        return lemmatized_output

    def removeEmojis(self, text: str) -> str:
        regrex_pattern = re.compile(pattern="["
                                            u"\U0001F600-\U0001F64F"  # emoticons
                                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                            "]+", flags=re.UNICODE)
        return regrex_pattern.sub(r'', text)

