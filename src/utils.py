"""Utility functions for a map-group-reduce action.

Author: Josh Borthick

_get_cpu_count
Returns the number of physical cores on the device.

_map_it
Extracts the document number and creates the tuple of
(term, (docID, 1)) for later summing into doc occurences.

_group_it
Groups terms alphabetically and combines into one tuple of
how many times that term occurs in each document in that 
term's listing.

_reduce_it
Adds the docID and that terms' per-document frequency to its 
linked list and returns that list.

_chunks
Creates parallelizable chunks of files for processing.

_save_index
Saves the postings to a pickle file.

_load_index
Loads the postings from a pickle file.

greeting
Prints a greeting to the screen.
"""

from itertools import groupby
from psutil import cpu_count
import pickle


def _get_cpu_count():
    """Return the number of physical CPUs."""
    return cpu_count(logical=False)


def _map_it(filename, terms):
    """Map file text to (term, (docID, 1))."""
    doc_id = int(filename.name.split("_")[1].split(".")[0])
    return list(map(lambda term: (term, (doc_id, 1)), terms))


def _group_it(sorted_terms):
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


def _reduce_it(term, llist):
    """Add term's docID and count to linked list.
    
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


def _chunks(files, n_batches):
    batch_size = (len(files) + n_batches - 1) // n_batches

    return [
        files[start:start + batch_size]
        for start in range(0, len(files), batch_size)
    ]


def _save_index(pkl_file, postings):
    """Save inverted index as pickle file."""
    with open(pkl_file, "wb") as pf:
        pickle.dump(postings, pf)


def _load_index(pkl_file):
    """Load inverted index from pickle file."""
    with open(pkl_file, "rb") as pf:
        postings = pickle.load(pf)
    return postings


def greeting():
    print("\n=================== CSC734-IR Homework 01 ==============\n"
          + "First Name: Josh\n"
          + "Last Name : Borthick\n"
          + "========================================================\n")
