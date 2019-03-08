from time import sleep

import requests
from bs4 import BeautifulSoup

# Wait time if connection refused
long_wait = 60


def get_soup_from_url(url):
    connection_made = False
    page = None
    while connection_made is False:
        try:
            page = requests.get(url)
        except requests.exceptions.RequestException:
            print("Connection refused.\nWaiting 60 seconds...")
            connection_made = False
            sleep(long_wait)
        else:
            connection_made = True

    soup = BeautifulSoup(page.content.decode('utf8', 'ignore'), 'html.parser')

    return soup
