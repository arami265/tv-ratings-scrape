import re


def get_year_from_span(string):
    string = re.sub('[^0-9]', '', string)
    string = string[0:4]

    return string


def make_alphanumeric_for_filename(title_string):
    # Deletes all special characters except for " -_"
    title_string = re.sub('[ ]+', '_', title_string)
    title_string = re.sub('[-]+', '_', title_string)
    title_string = re.sub('[^0-9a-zA-Z_]+', '', title_string)
    title_string = re.sub('[_]+', '_', title_string)

    title_string = title_string.lower()

    return title_string
