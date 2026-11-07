import json
import os

"""
Helper to print out stats in terminal
"""

def count_documents(doc_map_filepath: str) -> int:
    """
    This function returns how many documents were indexed.
    The doc map has one entry per document, so we just count the entries.
    """
    with open(doc_map_filepath, "r", encoding="utf-8") as the_file:
        doc_map = json.load(the_file)
    return len(doc_map)


def count_unique_terms(index_filepath: str) -> int:
    """
    This function returns how many unique terms are in the final index.
    Each line in the final index is a different term, so we count the lines.
    """
    count = 0

    # go through the file one line at a time instead of loading the whole thing
    with open(index_filepath, "r", encoding="utf-8") as the_file:
        for line in the_file:
            count += 1
    return count


if __name__ == "__main__":
    doc_map_filepath = "index_output/doc_map.json"
    index_filepath = "index_output/final_index.txt"

    num_docs = count_documents(doc_map_filepath)
    num_terms = count_unique_terms(index_filepath)

    # the size of the index on disk is the final index plus the doc map
    # getsize returns bytes so divide 1024 to get KB
    size_kb = (os.path.getsize(index_filepath) + os.path.getsize(doc_map_filepath)) / 1024

    print("Number of indexed documents:", num_docs)
    print("Number of unique words:", num_terms)
    print("Total index size (KB):", round(size_kb, 2))
