from pathlib import Path
from parser import parse_document, read_document
from urllib.parse import urldefrag

def get_json_files(dataset_path: str) -> list[Path]:
    """
    This function finds all JSON files in the dataset and returns
    their paths in a consistent order.
    """
    # create a Path object for the dataset directory
    dataset = Path(dataset_path)

    # find all JSON files, including those in subdirectories
    # rglob() stands for recursive glob. It searches the driectory
    # and all subdirectories for files matching *.json
    json_files = list(dataset.rglob("*.json"))

    # sort the files to ensure a consistent ordering
    json_files.sort()

    return json_files


def build_document_map(json_files: list[Path]) -> dict[int, str]:
    """
    This function assigns each JSON document a unique integer ID and
    returns a dictionary mapping document IDs to URLs.
    """
    # dictionary mapping document IDs to URLs
    doc_map: dict[int, str] = {}

    # loop through each JSON file and assign a doc ID
    for doc_id, filepath in enumerate(json_files):
        # read the JSON document
        document = read_document(str(filepath))

        # extract the URL and remove any fragments
        url = urldefrag(document["url"]).url

        # associate the document ID iwth its URL
        doc_map[doc_id] = url

    return doc_map


def build_partial_index(inverted_index: dict[str, list[tuple[int, int, int]]], doc_id: int, 
                        term_frequencies: dict[str, tuple[int, int]]) -> None:
    """
    This function adds one document's term frequenceis to the inverted index.
    Each postinf contains (doc_id, total_frequency, important_frequency).
    """
    # loop through each term and its frequencies
    for term, (total_count, important_count) in term_frequencies.items():
        # create an empty postings list if the term is not in the index
        if term not in inverted_index:
            inverted_index[term] = []

        # append the posting for this document
        inverted_index[term].append((doc_id, total_count, important_count))


def write_partial_index(inverted_index: dict[str, list[tuple[int, int, int]]], 
                        filepath: str) -> None:
    """
    This function writes an inverted index to a partial index file, where
    terms are sorted alphabetically and each posting contains
    document ID, total frequency, and important frequency.
    """                        
    # open the output file for writing
    with open(filepath, 'w', encoding="utf-8") as the_file:

        # loop through the terms in sorted order
        for term in sorted(inverted_index):

            # get the postings list for the term
            postings = inverted_index[term]

            # convert each posting into doc_id:total_frequency:important_frequency fromat
            posting_strings = []

            for doc_id, total_count, important_count in postings:
                posting_strings.append(
                    f"{doc_id}:{total_count}:{important_count}"
                )

            # join the postings with commas
            postings_text = ",".join(posting_strings)

            # write the term an its postings on one line then move to the next
            the_file.write(f"{term}\t{postings_text}\n")

if __name__ == "__main__":
    inverted_index = {}

    build_partial_index(
        inverted_index,
        0,
        {"comput": (2, 1), "scienc": (3, 1)}
    )

    build_partial_index(
        inverted_index,
        1,
        {"comput": (1, 0), "uci": (2, 1)}
    )

    print(inverted_index)

    write_partial_index(inverted_index, "test_partial.txt")

    with open("test_partial.txt", "r", encoding="utf-8") as the_file:
        print(the_file.read())