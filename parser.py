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


def extract_important_text(html:str) -> str:
    """
    This function extracts text from important HTML tags.
    Important text for this assignment is:
    bold: <b> or <strong>
    headings: <h1>, <h2>, <h3>
    titles: <title>
    """
    # convert HTML string into a BeautifulSoup object
    converted_html = BeautifulSoup(html, "html.parser")

    # create a set that contains the important tags in it
    important_tags = {"title", "h1", "h2", "h3", "b", "strong"}

    # list that will contain all important text
    important_text = []

    # loop through HTML for any important tags
    for tag in converted_html.find_all(important_tags):
        # skip tags that are nested inside another important tag
        if tag.find_parent(important_tags) is not None:
            continue
        
        # extract the text
        important_text.append(tag.get_text(separator=" ", strip=True))

    # join the elements in the list back into one string separated by spaces
    return " ".join(important_text)


if __name__ == "__main__":
    html = """
    <html>
        <head><title>UCI Computer Science</title></head>
        <body>
            <h1>Welcome to UCI</h1>
            <p>Computer Science is a popular major.</p>
            <strong>Apply today!</strong>
        </body>
    </html>
    """
    html2 = "<h1>Computer <strong>Science</strong></h1>"
    
    
    print(extract_important_text(html))
    print(extract_important_text(html2))
