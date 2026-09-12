"""Singly linked list and node classes.

Author: Josh Borthick
"""

class Node:
    """List node.
    
    ### Args:
        **doc_id: float**
        The docID, or -inf to start.  Compare docIDs for where to put
        each node.<br>

        **per_doc_term_freq: int**
        How many times that term occurs in that document.<br>

        **next: pointer**
        Points to the next node in the list.
    """

    def __init__(self, doc_id=float("-inf"), per_doc_term_freq=1, next=None):
        self.doc_id = doc_id
        self.per_doc_term_freq = per_doc_term_freq
        self.next = next


class LinkedList:
    """A linked list to hold (docID, term frequency) tuples.
    
    Checks document id (filename-number) for insert order.

    ### Args:
        **head: Node**
        Dummy, or sentinel head pointing to the first item, if any.<br>

        **doc_ids: int**
        The total number of documents the term is referenced in.<br>

        **total_freq: int**
        The total number of times the term is referenced.

    ### Methods:
        **add_node((docID, term_freq)): Node**
        Take a tuple containing docID and that term's frequency in 
        that document. Add that node to the list in order of docID.
        Return that node.<br>

        **get_list(): Node**
        Return the sentinel head.<br>

        **print_values(): None**
        Display the linked list for a term.
    """

    def __init__(self):
        """Sentinel head."""
        self.head = Node()
        self.doc_ids = 0
        self.total_term_freq = 0

    def add_node(self, doc_freq):
        """Place new (docID, freq) node in order of docID.
        
        ### Args:
            **doc_freq: tuple[str, tuple[int, int]]**
            The term and its document ID and frequency in document.

        ### Returns:
            **Node[value, next]**
            Node object with (docID, term_freq) value and pointer to
            next node.
        """
        node = Node(doc_freq[0], doc_freq[1])

        trv = self.head

        while trv.next is not None and trv.next.doc_id < doc_freq[0]:
            trv = trv.next

        node.next = trv.next
        trv.next = node
        self.doc_ids += 1
        self.total_term_freq += doc_freq[1]

        return node

    def get_list(self):
        """Return list head for traversal."""
        return self.head

    def print_values(self):
        """Print all this list's nodes' values."""
        trv = self.head.next
        while(trv is not None):
            print((trv.doc_id, trv.per_doc_term_freq), end=" -> ")
            trv = trv.next
        print(".")