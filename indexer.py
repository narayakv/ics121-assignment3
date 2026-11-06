import json
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



def build_index(dataset_path: str, output_dir: str, batch_size: int = 15000) -> None:
    """
    This function builds the inverted index by processing documents in batches. Partial
    indexes are written to disk. 
    """
    # get all JSON files in sorted order
    json_files = get_json_files(dataset_path)[:5]

    # create the output directory if it doesn't exist
    output_path = Path(output_dir)
    # parents=True creates any missing parent directories too
    # exist_ok=True prevents an error if the folder already exists
    output_path.mkdir(parents=True, exist_ok=True)

    # initialize the document map and inverted index
    doc_map = {}
    inverted_index = {}

    # track how many partial indexes have been written
    partial_count = 0

    # process each document
    for doc_id, filepath in enumerate(json_files):

        # read the document and extract its URL
        document = read_document(str(filepath))
        url = urldefrag(document["url"]).url

        # map the document ID to its URL
        doc_map[doc_id] = url

        # parse the document to get its term frequencies
        term_frequencies = parse_document(str(filepath))

        # add the document's terms to the inverted index
        build_partial_index(inverted_index, doc_id, term_frequencies)

        # flush the inverted index after every batch
        # since doc_id starts at 0, add 1 and then modulo with
        # batch_size. When it equals 0 we have completed the batch
        if (doc_id + 1) % batch_size == 0:

            # create the filename for this partial index
            partial_filepath = output_path / f"partial_{partial_count}.txt"

            # write the partial index to disk
            write_partial_index(inverted_index, str(partial_filepath))

            # clrear the inverted index to free memory
            inverted_index.clear()

            # increment the number of partial indexes written
            partial_count += 1

    # write any remaining documents to a final partial index
    if inverted_index:
        partial_filepath = output_path / f"partial_{partial_count}.txt"
        write_partial_index(inverted_index, str(partial_filepath))
        inverted_index.clear()
        partial_count += 1

    # save the document map to a JSON file
    doc_map_filepath = output_path / "doc_map.json"

    with open(doc_map_filepath, "w", encoding="utf-8") as the_file:
        json.dump(doc_map, the_file)

if __name__ == "__main__":
    build_index("developer/DEV", "test_output", batch_size=2)