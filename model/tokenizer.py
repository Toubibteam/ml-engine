#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import unicodedata
import re
from nltk.stem.snowball import FrenchStemmer

from config import UNK

class Tokenizer:
    """ Tokenize sentences """


    """ Class attributes """
    # (int) number of instances created
    _instances = 0
    # (set) contains all the stopwords
    _stopwords = set()
    # (object) French stemmer
    _stemmer = FrenchStemmer()


    def __init__(self):
        if self.__class__._instances == 0:
            # load stopwords once for all
            folder = path.abspath(path.split(__file__)[0])
            with open(folder + '/data/stopwords.txt','r') as df :
                self.__class__._stopwords = df.read().strip().split('\n')
        self.__class__._instances += 1


    def tokenize(self, sentence):
        """ Transform a sentence into tokens

        Args:
            sentence: (string)

        Returns:
            tokens: (list)

        """
        if sentence is None or isinstance(sentence, (int, long)):
            return [UNK]

        # remove accents
        s = self.remove_accents(sentence)
        # remove punctuation
        s = re.sub('[^-\w]', ' ', s)
        # convert to lower case
        s = s.lower()
        # split by words and remove empty strings
        tokens = s.split()
        # stem words
        tokens = [ self.__class__._stemmer.stem(t) for t in tokens ]
        # remove stop words
        tokens = [ t for t in tokens if not t in self.__class__._stopwords ]
        return tokens


    def remove_accents(self, sentence):
        """ Remove accents

        Args:
            sentence: (string) with accents

        Returns:
            cleaned_sentence: (string) sentence cleaned from accents

        """
        if type(sentence) is not unicode: sentence = unicode(sentence, 'utf-8')
        cleaned_sentence = unicodedata.normalize('NFKD', sentence)
        cleaned_sentence = cleaned_sentence.encode('ASCII', 'ignore')
        return cleaned_sentence
