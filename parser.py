import json



def read_document(filepath: str) -> dict:
    """ 
    This function takes in a filepath as a string and
    extracts and tokenizes HTML text from it.
    """
    with open(filepath, "r", encoding="utf-8") as the_file:
        document = json.load(the_file)

    return document