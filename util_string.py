import re


def make_alphanumeric_for_filename(str):
    # Deletes all special characters except for " -_"
    str = re.sub('[^0-9a-zA-Z_ -]+', '', str)

    # Replaces " -_" with "_"
    str = re.sub('[ -]+', '_', str)

    str = str.lower()

    return str
