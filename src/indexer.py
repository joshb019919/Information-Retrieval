"""Inverted index class for terms and linked list of docIDs.

Author: Josh Borthick
"""
import pickle

from linked_list import LinkedList
from normalizer import Normalize
from utils import _map_it, _group_it, _reduce_it

class Index:
    """An inverted index as a dictionary and linked list.
    
    Each term from the documents is a key.  Each document's id and that
    term's frequency in that document are nodes in a linked list.

    Methods are organized in stream-like format so that operations can
    be chained.

    The postings can technically be any structure and the postings list
    can technically be any container, but this class is currently not
    implemented for utilizing any objects other than a dictionary and
    linked list.

    ### Args:
        **normalizer: Normalizer | class**
        The normalizer class to use for normalizing the terms.<br>

        **filedir: str**
        The name of the directory to search for documents.<br>

        **stopfile: str**
        The name of the file containing the stopwords to remove from 
        terms.<br>

        **postings: dict**
        An empty or supplied dictionary of term: LinkedList pairs.

    ### Methods:
        **build_index(): Index**
        Generate the postings and lists and return the postings.<br>

        **get_all_postings(): None**
        Display all postings and their lists.<br>

        **get_posting(term): None**
        Display a single term's postings list.<br>

        **get_postings(terms): None**
        Display a selection of term's postings lists.<br>

        **get_top_n(n): list[tuple[str, int]]**
        Return the terms with the top n largest postings lists.<br>

        **load_index(pkl_file, stopfile): dict[str, LinkedList]**
        Return the dictionary of postings.<br>

        **save_index(pkl_file): None**
        Save a postings dictionary to file as a pickle.
    
    ### Examples:
        `index = Index("dir", "stopwords.txt")`
        `index.build_index()`<br>
        
        `index.get_all_postings()`
        *{term: [(1, 3), (2, 1), (7, 2)]}*<br>

        `print(len(index.get_all_postings()))`
        *1*<br>

        `index.build_index().get_all_postings()`
        *{term: [(1, 3), (2, 1), (7, 2)]}*<br>

        `[{i: self.postings[i].doc_ids} for i in list(self.postings)[-1:-n-1:-1]]`
        *[{term1: 688, term2: 604, ...}]*
    """
    def __init__(self, files, stopfile, parent_dir="files/documents", 
                 postings_list=LinkedList, postings={}, normalizer=Normalize):
        self.normalizer = normalizer(stopfile)
        self.files = files
        self.stopfile = stopfile
        self.postings = postings
        self.postings_list = postings_list
        self.parent_dir = parent_dir

    def build_index(self):
        """Create the postings dictionary and term lists."""
        for file in self.files:
            tokens = self.normalizer.get_tokens(file)
            mapped_terms = _map_it(file, tokens)
            grouped_terms = _group_it(mapped_terms)

            for term in grouped_terms:
                if self.postings.get(term[0], None) is None:
                    self.postings[term[0]] = self.postings_list()
                _reduce_it(term, self.postings[term[0]])

        # Sort in order of linked list length
        self.postings = dict(sorted(self.postings.items(), 
                                    key=lambda term: term[1].doc_ids))

        return self

    def get_top_n(self, n):
        """Print the top n most frequently documented terms and the
        number of document IDs in their postings list."""
        print(self.postings["044"].total_term_freq)
        sorted_postings = sorted(self.postings.items(), 
                      key=lambda posting: self.postings[posting[0]].total_term_freq, 
                      reverse=True)
        return [p[0] for p in sorted_postings[:n]]

    def get_all_postings(self):
        """Print out all postings lists."""
        for posting in self.postings:
            print(posting, end="\t")
            self.postings[posting].print_values()

    def get_posting(self, term):
        """Print one term's postings list."""
        self.postings[term].print_values()

    def get_postings(self, terms):
        """Print each term's posting list."""
        for term in terms:
            self.postings[term].print_values()

    def save_index(self, pkl_file):
        """Save inverted index as pickle file."""
        with open(pkl_file, "wb") as pf:
            pickle.dump(self.postings, pf)

    def load_index(self, pkl_file, stopfile):
        """Load inverted index from pickle file."""
        index = Index("", stopfile)
        with open(pkl_file, "rb") as pf:
            index.postings = pickle.load(pf)
        return index
