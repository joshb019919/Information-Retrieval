# Information-Retrieval

Project for MSU CSC734 Information Retrieval and beyond!

## Dependencies

### Built-In Dependencies
- concurrent
- itertools
- pathlib
- pickle
- sys
- re
- string

### Installed Dependencies
- nltk
- psutil

#### Be careful using Conda.

I did not use Conda to manage environments and dependencies, so there is a `requirements.txt` file containing the necessary environment specification.  The CSC734_IR.yml file does not contain `psutil`.

## Version 

Python 3.13.5

## License

Apache 2.0

## Run this program from root extracted dir!

This project takes in a directory of files and builds an inverted index as a dictionary of terms and their postings lists.  Postings lists are singly linked lists without skip pointers.

Each node in the postings lists contain the document id, the per-document term frequency, and the next pointer.  The list also tracks total documents per term and the total term frequency across all documents.

## Usage
`python src/main.py`

The inverted index is automatically generated and all necessary displays are output to the console.  *Both concurrent and parallel statistics are printed.*

## Other functions

The other functions and methods can be utilized freely, but user beware as it's not made for it.

Different types of postings lists and normalizers can be substituted for their defaults contained in this project, so long as they adhere to the calling class's method structure.

### Different normalizer

Must implement `get_tokens(filename)`, which must return a list of strings.

### Different postings list object

Must implement `add_node(docID)`, `get_list()`, and `print_values()`.  They must return a Node, Node, and Any | None, respectively.  Currently, it is not intended to work with anything other than a node class, but the list itself may be a different object class.  If it is, it must also store data in `((docID, term_freq_per_doc), next)` Nodes.

## Warning

This program does not guarantee it will work on any other Python version, environment, or operating system (though it should).  If parts are substituted such as a separate normalizer, there is no guarantee that the `main()` function will work without alterations or additions.

## AI Use Statement

Parallelizing by multiprocessing is not taught or expected at MSU, so I had not learned it till this project.  The following are prompts and their responses from Duck.ai.  Light gray are prompts, black is response.

### I did not use all of this tutorial in the code.

- <span style="color:#999;"> Please provide a tutorial about parallel multiprocessing in Python.  Use examples for passing in text files and combining the intermediate results into a dictionary.</span>

### Parallel multiprocessing in Python

Python’s multiprocessing module lets you run CPU-bound work across multiple processes. Each process has its own Python interpreter and memory, so it can bypass the Global Interpreter Lock (GIL).

A common pattern is:

- Find input files.
- Send each file to a worker process.
- Return an intermediate result from each worker.
- Combine those results into one dictionary in the parent process.

The example below counts words across multiple text files.

### Example directory

```Text
project/
├── parallel_word_count.py
└── texts/   
├───── file1.txt    
├───── file2.txt    
└───── file3.txt
```

### Complete example

```Python
from collections import Counter
from multiprocessing import Pool, cpu_count
from pathlib import Path
import re


def count_words_in_file(file_path):
    """
    Worker function.

    Receives one file path and returns an intermediate dictionary
    containing word counts for that file.
    """
    counts = Counter()

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # Extract words and normalize them to lowercase.
            words = re.findall(r"\b[\w']+\b", line.lower())
            counts.update(words)

    return dict(counts)


def combine_dictionaries(partial_results):
    """
    Combine dictionaries returned by worker processes.
    """
    combined = Counter()

    for partial_result in partial_results:
        combined.update(partial_result)

    return dict(combined)


def main():
    input_directory = Path("texts")
    file_paths = list(input_directory.glob("*.txt"))

    if not file_paths:
        print("No text files found.")
        return

    # Use one worker per CPU core, up to the number of files.
    worker_count = min(cpu_count(), len(file_paths))

    with Pool(processes=worker_count) as pool:
        # Each file path is passed to count_words_in_file().
        partial_results = pool.map(count_words_in_file, file_paths)

    final_counts = combine_dictionaries(partial_results)

    for word, count in sorted(
        final_counts.items(),
        key=lambda item: item[1], reverse=True
    ):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
```

Run it with:

```Bash
python parallel_word_count.py
```

The output might look like:

```Json
python: 12
data: 9
process: 7
file: 6
```

### How the multiprocessing works

This line creates a process pool:

```Python 
with Pool(processes=worker_count) as pool:
```

If your computer has eight CPU cores and there are eight files, the pool may create eight worker processes.

This line distributes the file paths among the workers:

```Python 
partial_results = pool.map(count_words_in_file, file_paths)
```

Conceptually, it performs work similar to:

```Python 
result_1 = count_words_in_file("texts/file1.txt")
result_2 = count_words_in_file("texts/file2.txt")
result_3 = count_words_in_file("texts/file3.txt")
```

The difference is that the calls happen in parallel processes.

Each worker returns an independent dictionary, such as:

```Python
{"python": 3, "data": 2}
```

The parent process then combines the dictionaries:

```Python 
combined.update(partial_result)
```

For example:

```Python
{"python": 3, "data": 2}
{"python": 4, "file": 1}
```

becomes:

```Python
{"python": 7, "data": 2, "file": 1}
```

### Why use Counter?

Counter is a dictionary subclass designed for counting. It makes dictionary merging simple:

```Python
from collections import Counter
first = Counter({"python": 3, "data": 2})
second = Counter({"python": 4, "file": 1})
combined = first + second
print(combined)
```

Output:

```Python
Counter({'python': 7, 'data': 2, 'file': 1})
```

You can also write the combination step as:

```Python
def combine_dictionaries(partial_results):    
    combined = Counter()
    for partial_result in partial_results:        
        combined += Counter(partial_result)
    return dict(combined)
```

### Passing more than one argument to workers

`Pool.map()` passes one item at a time to the worker function. If each task needs multiple arguments, use `Pool.starmap()`.

For example, suppose each file should be read using a configurable encoding:

```Python
from multiprocessing import Pool

def count_words(file_path, encoding):    
    counts = {}
    with open(file_path, "r", encoding=encoding) as file:        
        for line in file:            
            for word in line.lower().split():                
                counts[word] = counts.get(word, 0) + 1
    return counts

def main():    
    tasks = [        
        ("texts/file1.txt", "utf-8"),        
        ("texts/file2.txt", "utf-8"),        
        ("texts/file3.txt", "utf-8"),    
        ]
    with Pool() as pool:        
        results = pool.starmap(count_words, tasks)
    combined = {}
    for result in results:        
        for word, count in result.items():            
            combined[word] = combined.get(word, 0) + count
    print(combined)

if __name__ == "__main__":    
    main()
```

Each tuple in tasks is unpacked and passed to the worker:

```Python
count_words("texts/file1.txt", "utf-8")
```

### Processing results as they finish

`pool.map()` returns results in the same order as the input files. If you do not need ordered results, `imap_unordered()` can process each result as soon as it becomes available:

```Python
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

def count_words_in_file(file_path):    
    counts = Counter()
    with open(file_path, "r", encoding="utf-8") as file:        
        for line in file:            
            counts.update(line.lower().split())
    return counts

def main():    
    file_paths = list(Path("texts").glob("*.txt"))    
    combined = Counter()
    with Pool() as pool:        
        for partial_result in pool.imap_unordered(            
                count_words_in_file, file_paths):            
            combined.update(partial_result)
    print(dict(combined))

if __name__ == "__main__":    
    main()
```

This can be useful when:

- Some files are much larger than others.
- You want to update progress as files finish.
- You do not care which file’s result arrives first.

### Using `apply_async`

For more control, use apply_async():

```Python
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

def count_words_in_file(file_path):    
    counts = Counter()
    with open(file_path, "r", encoding="utf-8") as file:        
        for line in file:            
            counts.update(line.lower().split())
    return dict(counts)

def main():    
    file_paths = list(Path("texts").glob("*.txt"))
    with Pool() as pool:        
        jobs = [            
            pool.apply_async(count_words_in_file, (file_path,))            
            for file_path in file_paths        
            ]
        partial_results = [job.get() for job in jobs]
    combined = Counter()
    for result in partial_results:        
        combined.update(result)
    print(dict(combined))

if __name__ == "__main__":    
    main()
```

`apply_async()` returns an `AsyncResult`. Calling:

```Python
job.get()
```

waits for the worker’s result and retrieves it.

### Returning results associated with filenames

Sometimes the intermediate result should include the input filename:

```Python
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

def process_file(file_path):    
    counts = Counter()
    with open(file_path, "r", encoding="utf-8") as file:        
        for line in file:            
            counts.update(line.lower().split())
    return {        
        "file": str(file_path),        
        "word_counts": dict(counts),    
        }

def main():    
    file_paths = list(Path("texts").glob("*.txt"))
    with Pool() as pool:        
        results = pool.map(process_file, file_paths)
    results_by_file = {        
        result["file"]: result["word_counts"]        
        for result in results    
        }
    for filename, counts in results_by_file.items():        
        print(filename)        
        print(counts)

if __name__ == "__main__":    
    main()
```

The final dictionary has this shape:

```Json
{    
    "texts/file1.txt": {        
        "python": 3,        
        "data": 2,    
    },    
    "texts/file2.txt": {        
        "python": 4,        
        "process": 1,    
    },
}
```

### Combining nested dictionaries

If the workers return nested dictionaries, you can combine them manually:

```Python
from collections import defaultdict

def combine_by_category(partial_results):    
    combined = defaultdict(dict)
    for partial_result in partial_results:        
        for category, values in partial_result.items():            
            if category not in combined:                
                combined[category] = {}
            for key, value in values.items():                
                combined[category][key] = (
                    combined[category].get(key, 0) + value                
                )
    return dict(combined)
```

For example, these intermediate results:

```Json
[    
    {        
        "file1.txt": {"python": 3, "data": 2}    
    },    
    {        
        "file2.txt": {"python": 4, "process": 1}    
    }
]
```

can be combined into:

```Json
{    
    "file1.txt": {"python": 3, "data": 2},    
    "file2.txt": {"python": 4, "process": 1},
}
```

### Important multiprocessing rules

Protect the entry point

Always put pool creation inside:

```Python
if __name__ == "__main__":
```

This is especially important on Windows and macOS, where new processes may import the main module again.

#### Worker functions should be top-level functions

Prefer this:

```Python
def process_file(path):    
    return result
```

#### Avoid defining the worker only inside main():

```Python
def main():    
    def process_file(path):        
        return result
```

Top-level functions are easier for multiprocessing to serialize and use in child processes.

#### Return values instead of modifying shared state

Avoid trying to modify a normal dictionary from multiple processes:

```Python
shared_results = {}
def worker(path):    
    shared_results[path] = process(path)
```

Each process has separate memory, so the parent process will not automatically see those changes.

Instead, return results:

```Python
def worker(path):    
    return path, process(path)
```

Then combine them in the parent process:

```Python
results = pool.map(worker, file_paths)
combined = dict(results)
```

### Do not create too many processes

A reasonable default is:

```
worker_count = min(cpu_count(), len(file_paths))
```

Creating hundreds of processes for a few files usually adds overhead rather than improving performance.

### Multiprocessing may not help for simple file reading

If the task mostly waits for disk or network I/O, threads may be more appropriate. Multiprocessing is most useful when each file requires substantial CPU work, such as:

- Parsing large documents
- Compressing data
- Computing hashes
- Transforming images
- Running expensive text analysis

For ordinary small text files, process startup and result-transfer overhead may outweigh the benefit.

### A reusable general pattern

The general design looks like this:

```Python
from multiprocessing import Pool

def worker(item):    
    # Process one input item.    
    return intermediate_result

def combine(results):    
    final_result = {}
    for result in results:        
        # Merge one intermediate result.        
        pass
    return final_result

def main():    
    inputs = [...]  
    # Files, records, URLs, or other work items.
    with Pool() as pool:        
        intermediate_results = pool.map(worker, inputs)
    final_result = combine(intermediate_results)    
    print(final_result)

if __name__ == "__main__":    main()
```

The key idea is to keep the worker independent:

```Text
input item → worker process → intermediate result → parent process → final dictionary
```

This approach avoids shared-memory complexity and makes the program easier to test, debug, and scale.
