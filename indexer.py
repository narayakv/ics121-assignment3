from pathlib import Path
from parser import parse_document

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


if __name__ == "__main__":
    json_files = get_json_files("developer/DEV")

    print("Total JSON files:", len(json_files))

    for filepath in json_files[:5]:
        print(filepath)