import json
from bs4 import BeautifulSoup


def read_document(filepath: str) -> dict:
    """ 
    This function takes in a path to a single JSON file as a string and
    reads the JSON document, returning its contents as a dictionary
    """
    with open(filepath, "r", encoding="utf-8") as the_file:
        document = json.load(the_file)

    return document


def extract_text(html: str) -> str:
    """ 
    This function extracts text from an HTML document.
    """
    # convert HTML string into a BeautifulSoup object
    converted_html = BeautifulSoup(html, "html.parser")

    # extract the text content and remove the HTML tags using get_text
    # insert a space as a separator between words so they don't accidentally get joined
    # and remove surrounding whitespace using strip
    text = converted_html.get_text(separator= " ", strip=True)

    return text