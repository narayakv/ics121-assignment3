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

if __name__ == "__main__":
    json_files = get_json_files("developer/DEV")

    # test with only five documents
    doc_map = build_document_map(json_files[:5])

    for doc_id, url in doc_map.items():
        print(doc_id, url)