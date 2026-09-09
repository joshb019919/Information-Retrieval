from functools import reduce
from itertools import groupby
from nltk import download
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from os import scandir
from sys import getsizeof
download('punkt_tab')


def map_it(filename, terms):
    """Map file text to (term, (docID, 1))."""
    doc_id = int(filename.split("_")[1].split(".")[0])
    return list(map(lambda term: (term, (doc_id, 1)), terms))


def group_it(sorted_terms):
    """Group sorted, mapped terms by (term, (docID, count in text))."""
    grouped_terms = groupby(sorted_terms, key=lambda item: item[0])
    terms = []
    for _, group in grouped_terms:
        group = list(group)
        freq = len(group)
        term = group[0][0]
        doc_id = group[0][1][0]
        terms.append((term, (doc_id, freq)))
    return terms


def reduce_it(term, llist):
    """Add term to linked list.
    
    Args:
        **term**: tuple[str, tuple[int, int]]
        The term with its document ID and frequency count.

    Returns:
        LinkedList
        The postings list for the dictionary term.
    """
    t = term[0]
    doc_freq = term[1]
    llist.add_node(doc_freq)
    return llist


class Node:
    """List node."""

    def __init__(self, value=float("-inf"), next=None):
        self.value = value
        self.next = next


class LinkedList:
    """A linked list to hold (docID, term frequency) tuples.
    
    Checks document id (filename-number) for insert order.
    """

    def __init__(self):
        """Sentinel head."""
        self.head = Node()
        self.list_size = 0

    def add_node(self, doc_freq):
        """Place new (docID, freq) node in order of docID.
        
        Args:
            **doc_freq**: tuple[str, tuple[int, int]] 
            The term and its document ID and frequency in document.
        """
        node = Node(doc_freq)

        trv = self.head

        while trv.next is not None and trv.next.value[0] < doc_freq[0]:
            trv = trv.next

        node.next = trv.next
        trv.next = node
        self.list_size += 1

    def get_list(self):
        """Return list head for traversal."""
        return self.head

    def print_values(self):
        """Print all this list's nodes' values."""
        trv = self.head.next
        while(trv is not None):
            print(trv.value, end=" -> ")
            trv = trv.next
        print(".")


class Normalizer:
    """Normalize all words by removing punctuation and stop words, then
    tokenizing and stemming them.
    """

    def __init__(self, filedir, stopfile):
        self.stemmer = PorterStemmer()
        self.stopwords = self.read_stopwords(stopfile)
        self.filedir = filedir
        self.postings = {}

    def read_file(self, fname):
        """Take text, lowercase, strip extra whitespace, make list.
        
        Args:
            **fname**: str
            The dynamically assigned file path to open.

        Returns:
            list[str]
            Lower-cased, stripped list of words in document.    
        """
        with open(fname, "r") as f:
            return f.read().lower().strip().replace("  ", " ").split()

    def read_stopwords(self, fname):
        """Get stop words as one list.
        
        Args:
            **fname**: str
            The manually assigned file path to open.
        
        Returns:
            list[str]
            A list of the stop words to remove from tokens.
        """
        with open(fname, "r") as f:
            return [word.replace("\n", "") for word in f.readlines()]
        
    def normalize_terms(self, file, stops):
        """Tokenize with NLTK, remove punctuation, and stem.
        
        Args:
            **file**: list[str]
            The word list from read_file.

            **stops**: list[str]
            The list of stop words from read_stopwords.

        Returns:
            list[str]
            The words from the text, but with no punctuation or stop 
            words and stemmed and tokenized with NLTK.
        """
        return [self.stemmer.stem(word) for word in word_tokenize(
            " ".join([word for word in file if word not in stops]))
            if word not in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"]

    def get_tokens(self, file):
        """Return the normalized terms in ascending order.
        
        Args:
            **file**: os.scandir DirEntry[str]
            The file to read.

        Returns:
            list[str]
            The sorted, normalized tokens from the document.    
        """
        txt = self.read_file(file.path)
        return sorted(self.normalize_terms(txt, self.stopwords))


class Indexer:
    def __init__(self, filedir, stopfile):
        self.normalizer = Normalizer(filedir, stopfile)
        self.filedir = filedir
        self.stopfile = stopfile
        self.postings = {}   

    def insert_term(self, term):
        """Insert a term into the dictionary in order of list length.
        
        TODO"""  
        pass

    def build_index(self):
        """Create the postings dictionary and term lists."""
        for file in scandir(self.filedir):
            tokens = self.normalizer.get_tokens(file)
            mapped_terms = map_it(file.name, tokens)
            grouped_terms = group_it(mapped_terms)

            for term in grouped_terms:
                if self.postings.get(term[0], None) is None:
                    self.postings[term[0]] = LinkedList() 
                reduce_it(term, self.postings[term[0]])

        # Sort in order of linked list length
        self.postings = dict(sorted(self.postings.items(), 
                                    key=lambda term: term[1].list_size))

    def get_all_postings(self):
        """Print out all postings lists."""
        for posting in self.postings:
            print(posting, end="\t")
            self.postings[posting].print_values()

    def get_posting(self, term):
        """Print one term's postings list."""
        self.postings[term].print_values()


def main():
    # indexer = Indexer("testdir1", "stopwords.txt")
    # indexer = Indexer("testdir2", "stopwords.txt")
    indexer = Indexer("documents", "stopwords.txt")

    # term = "missouri"
    # doclist = [8, 1, 4, 1, 5, 9, 10]
    # for doc in doclist:
    #     indexer.add_doc_id(term, doc)
    # indexer.get_all_postings()

    indexer.build_index()
    postings = indexer.postings
    psize = getsizeof(postings)
    print("Index Size")
    print(f"{psize} B")
    print(f"{psize/1024**2:.3f} MB")

    # print(indexer.get_all_postings())   
    # print(len(indexer.postings.keys()))

if __name__ == "__main__":
    print("\n=================== CSC734-IR Homework 01 ==============\n"
          + "First Name: Josh\n"
          + "Last Name : Borthick\n"
          + "========================================================\n")
    main()
