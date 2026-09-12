"""Normalizer class for words.

Author: Josh Borthick
"""
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

import re
import string

class Normalize:
    """Normalize all words by removing punctuation and stop words, then
    tokenize and stem them.  Uses PorterStemmer by default.

    ### Args:
        **stemmer: class**
        The stemmer object to stem terms.<br>

        **stopwords: str**
        The text file containing words to remove from the terms list.

    ### Methods:
        **_read_file(fname): list[str]**
        Read file fname and return each word in a list of strings.<br>

        **_read_stopwords(fname): list[str]**
        Read the stopwords file and return them in a list of strings.<br>

        **_normalize_terms(file, stops): list[str]**
        Normalize all terms and return them in a list of strings.<br>

        **get_tokens(file): list[str]**
        Read in tokens and return them normalized and in ascending order.
    """

    def __init__(self, stopfile, stemmer=PorterStemmer()):
        self.stemmer = stemmer
        self.stopwords = self._read_stopwords(stopfile)
        self.punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    def _read_file(self, fname):
        """Take text, lowercase, strip extra whitespace, make list.
        
        ### Args:
            **fname: str**
            The dynamically assigned file path to open.

        ### Returns:
            **list[str]**
            Lower-cased, stripped list of words in document.    
        """
        with open(fname, "r") as f:
            return f.read().lower().strip().replace("  ", " ").split()

    def _read_stopwords(self, fname):
        """Get stop words as one list.
        
        ### Args:
            **fname: str**
            The manually assigned file path to open.
        
        ### Returns:
            **list[str]**
            A list of the stop words to remove from tokens.
        """
        with open(fname, "r") as f:
            return [word.replace("\n", "") for word in f.readlines()]
        
    def _normalize_terms(self, file, stops):
        """Tokenize with NLTK, remove punctuation, and stem.
        
        ### Args:
            **file: list[str]**
            The word list from _read_file.<br>

            **stops: list[str]**
            The list of stop words from _read_stopwords.

        ### Returns:
            **list[str]**
            The words from the text, but with no punctuation or stop 
            words and stemmed and tokenized with NLTK.
        """
        return [self.stemmer.stem(word) for word in word_tokenize(
            " ".join([re.sub(f"[{re.escape(string.punctuation)}]+", " ", word) 
                      for word in file if word not in stops]))]

    def get_tokens(self, file):
        """Return the normalized terms in ascending order.
        
        ### Args:
            **file: os.scandir DirEntry[str]**
            The file to read.

        ### Returns:
            **list[str]**
            The sorted, normalized tokens from the document.    
        """
        txt = self._read_file(file)
        
        return sorted(self._normalize_terms(txt, self.stopwords))