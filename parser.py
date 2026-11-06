import json
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer


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

    # remove non-content HTML elements
    for tag in converted_html(["script", "style", "noscript", "template"]):
        tag.decompose()

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

    # remove non-content HTML elements
    for tag in converted_html(["script", "style", "noscript", "template"]):
        tag.decompose()

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


# The runtime complexity is linear: O(n), where n is the number of characters in the text.
# Each character is examined exactly once while this function tokenizes the text.
def tokenize(text: str) -> list[str]:
    """
    This function takes text as a string and returns a list
    of strings called tokens. Each character of the text is examined and becomes either
    part of a token or a separator. Tokens are strings of alphanumeric characters
    that are separated by a separator. A separator is defined as any character that is not
    alphanumeric; these characters will not be included in tokens, but they signal the end of a token.
    Since a token is only added once a separator is hit, we need one last check to see if there are 
    character(s) in the current list that have not been added to the tokens list because we reached the 
    end of the text without a separator.
    """
    # initialize an empty list of tokens
    tokens: list[str] = []
    # initialize an empty list that represents the current token
    current: list[str] = []

    # loop through the text
    for char in text:
        # char is alphanumeric
        if ('a' <= char.lower() <= 'z' or '0' <= char <= '9'):
            # append a lowercase version of the char so tokens become independednt of capitalization
            current.append(char.lower())
        else:
            # otherwise, the character is not part of the token and becomes a separator 
            if (len(current) >= 1):
                # append the current token but only if there is actually something in it
                # join each single character string into a combined string separated by "",
                # which is an empty string, so ['a', 'b'] becomes "ab"             
                tokens.append("".join(current))
            # reset current
            current = []

    # the end of the text has been reached
    # there might still be a token left over if the last character is not a separator
    if (len(current) >= 1):
        tokens.append("".join(current))

    return tokens


# define a PorterStemmer object
stemmer = PorterStemmer()
def stem_tokens(tokens: list[str]) -> list[str]:
    """
    This function applies Porter Stemming to a list of tokens.
    """
    # list that will contain stemmed tokens
    stemmed_tokens = []

    # loop through the tokens
    for token in tokens:
        # append the stemmed token to the stemmed_tokens list
        stemmed_tokens.append(stemmer.stem(token))

    return stemmed_tokens


# The runtime complexity of this function is linear: O(n), where n is the number of tokens 
# in the tokens list. Each token is examined exactly once, and dictionary lookup (when 
# we do token in word_frequencies) and insertion are both O(1) on average.
def compute_word_frequencies(tokens: list[str]) -> dict[str, int]:
    """
    This function takes in a list of strings and returns a dictionary of 
    string keys and integer values. The keys are tokens and the integer values
    are the frequency at which they appear in the list. We check to see if the
    token is already in the dictionary, and if it is we add one to the frequency.
    If it is not, we initialize that token as a key with a frequency value of 1.
    """
    # initialze an empty dict with a str key and an int value
    word_frequencies: dict[str, int] = {}
    for token in tokens:
        # check if the token is already in the dictionary
        # if it is then you can just add 1 to the value, but if not
        # you need to initialize the key to 1
        if (token in word_frequencies):
            word_frequencies[token] += 1
        else:
            word_frequencies[token] = 1

    return word_frequencies



def parse_document(filepath: str) -> dict[str, tuple[int, int]]:
    """
    This function parses a JSON webpage and returns a dictionary mapping
    each stemmed token to its total frequency and important frequency.
    """
    # read the JSON document
    document = read_document(filepath)

    # get the HTML content
    html = document["content"]

    # extract all text and important text
    all_text = extract_text(html)
    important_text = extract_important_text(html)

    # tokenize the regular and important text
    all_tokens = tokenize(all_text)
    important_tokens = tokenize(important_text)

    # apply Porter stemming to both lists of tokens
    stemmed_tokens = stem_tokens(all_tokens)
    stemmed_important_tokens = stem_tokens(important_tokens)

    # count the occurrences of each stemmed token
    total_frequencies = compute_word_frequencies(stemmed_tokens)
    important_frequencies = compute_word_frequencies(stemmed_important_tokens)

    # dictionary mapping each stemmed token to its total and important frequency
    term_frequencies: dict[str, tuple[int, int]] = {}

    # loop through every token and its total frequency
    for token, total_count in total_frequencies.items():
        # get the important frequency, or 0 if the token is not important
        important_count = important_frequencies.get(token, 0)

        # store both frequencies as a tuple
        term_frequencies[token] = (total_count, important_count)

    return term_frequencies
