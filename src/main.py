"""Build, store, load, and parse inverted indexes.

Author: Josh Borthick
Date Completed: 9/12/2026
"""
import pathlib
from nltk import download
download('punkt_tab')

from concurrent.futures import ProcessPoolExecutor
from sys import getsizeof
from indexer import Index
from utils import greeting, _get_cpu_count, _chunks, _save_index, _load_index


def main(files):
    """Create the index object and build the inverted index."""
    indexer = Index(files, "files/stopwords.txt")

    # Build index
    indexer.build_index()

    return indexer
    

if __name__ == "__main__":
    import time

    # Display header
    greeting()

    ############################ SHARED ##############################
    index = {}                                                       #
    directory = pathlib.Path("files/documents").resolve()            #
    files = [path for path in directory.iterdir() if path.is_file()] #
    batches = _chunks(files, _get_cpu_count())                       #
    ##################################################################


    ###################### CONCURRENT PROCESSING #####################
    start = time.time_ns()                                           #
    concurrent = main(files)                                         #
    stop = time.time_ns()                                            #
                                                                     #
    #########################                                        #
    # CONCURRENT STATISTICS #                                        #
    #########################                                        #
    print("\n\n==============================")                      #
    print("PRINTING CONCURRENT STATISTICS")                          #
    print("==============================\n")                        #
    postings = concurrent.postings                                   #
    psize = getsizeof(postings)                                      #
                                                                     #
    # Display index size in bytes and MB                             #
    print("Index Size")                                              #  
    print("==========")                                              #
    print(f"{psize} B")                                              #
    print(f"{psize/1024**2:.3f} MB")                                 #
    print()                                                          #
                                                                     #
    # Display total terms in postings dictionary                     #
    print("Total Terms")                                             #
    print("===========")                                             #
    print(len(concurrent.postings.keys()))                           #
    print()                                                          #
                                                                     #
    # Display top_n function                                         #
    top_n = concurrent.get_top_n(5)                                  #
    print("Top n Terms (by total docIDs)")                           #
    print("=============================")                           #
    for n in top_n:                                                  #
        print(n)                                                     #
                                                                     #
    print()                                                          #
                                                                     #
    # Demonstrate saving and loading the inverted index pickle file  #
    concurrent.save_index("concurrent_index.pkl")                    #
    loaded_index = Index.load_index(Index, "concurrent_index.pkl",   #
                                    "files/stopwords.txt")           #
    top_n = loaded_index.get_top_n(5)                                #
                                                                     #
    print("Top n Terms of Loaded File")                              #
    print("==========================")                              #
    print(top_n)                                                     #
    ##################################################################

    ######################## MULTIPROCESSING #########################
    # There is overhead, but much faster                             #
    start_mp = time.time_ns()                                        #
    with ProcessPoolExecutor(_get_cpu_count()) as pool:              #
        parallel = pool.map(main, batches)                           #
    stop_mp = time.time_ns()                                         #
                                                                     #
    for e in enumerate(parallel):                                    #
        index.update(e[1].postings)                                  #
                                                                     #
    #######################                                          #
    # PARALLEL STATISTICS #                                          #
    #######################                                          #
    print("\n\n============================")                        #
    print("PRINTING PARALLEL STATISTICS")                            #
    print("============================\n")                          #
                                                                     #
    postings = concurrent.postings                                   #
    psize = getsizeof(postings)                                      #
                                                                     #
    # Display index size in bytes and MB                             #
    print("Index Size")                                              #
    print("==========")                                              #
    print(f"{psize} B")                                              #
    print(f"{psize/1024**2:.3f} MB")                                 #
    print()                                                          #
                                                                     #
    # Display total terms in postings dictionary                     #
    print("Total Terms")                                             #
    print("===========")                                             #
    print(len(concurrent.postings.keys()))                           #      
    print()                                                          #
                                                                     #
    # Display top_n function                                         #
    top_n = concurrent.get_top_n(5)                                  #
    print("Top n Terms (by total docIDs)")                           #
    print("=============================")                           #
    for n in top_n:                                                  #
        print(n)                                                     #
                                                                     #
    print()                                                          #
                                                                     #
    # Demonstrate saving and loading the inverted index pickle file  #
    _save_index("parallel_index.pkl", index)                         #
    loaded_index = _load_index("parallel_index.pkl")                 #
    loaded_index = Index(files, "files/stopwords.txt", postings=index)
    top_n = loaded_index.get_top_n(5)                                #
                                                                     #
    print("Top n Terms of Loaded File")                              #
    print("==========================")                              #
    print(top_n)                                                     #
    ##################################################################

    print(f"\nMultiprocessing time: {stop_mp / 1000000 - start_mp / 1000000:.4f} ms")
    print(f"Single process time: {stop / 1000000 - start / 1000000:.4f} ms")
