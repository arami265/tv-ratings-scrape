import requests
from time import sleep
from bs4 import BeautifulSoup
import json
import util_string


def scrape_shows():
    # Gets the most popular TV shows from IMDB
    connection_made = False
    while connection_made is False:
        try:
            page = requests.get("https://www.imdb.com/chart/tvmeter?ref_=nv_tvv_mptv")
        except requests.exceptions.ConnectionError:
            print("Connection refused.\nWaiting 60 seconds...")
            connection_made = False
            sleep(60)
        else:
            connection_made = True

    soup = BeautifulSoup(page.content.decode('utf8', 'ignore'), 'html.parser')

    # Gets all the rows of the tbody containing all the shows
    tr_show_items = soup.find('tbody', {'class': 'lister-list'}).findChildren('tr', recursive=False)

    # Extract title, year, rating, and IMDB link from each show
    for tr in tr_show_items:
        show = get_show_as_dict(tr)

        title = util_string.make_alphanumeric_for_filename(show['title'])
        file_name = '.\\shows\\' + title + '_' + show['year'] + '.json'

        with open(file_name, 'w') as outfile:
            json.dump(show, outfile)


def get_show_as_dict(tr):
    """
    Receives an IMDB page with a list of shows and returns a dict
    :param tr:
    :return:
    Returns a dict with the show's information
    """
    title_column = tr.find('td', {'class': 'titleColumn'})
    title = title_column.a.contents[0]
    href = title_column.a["href"]
    year = title_column.span.contents[0]
    year = year.replace('(', '')
    year = year.replace(')', '')

    rating_column = tr.find('td', {'class': 'ratingColumn imdbRating'})
    if rating_column.strong is not None:
        rating = rating_column.strong.contents[0]
    else:
        rating = None

    # Get all episodes from the current show
    show_url = 'https://www.imdb.com' + href
    seasons_and_description = get_seasons_and_description(show_url)

    show_description = seasons_and_description['show_description']
    seasons = seasons_and_description['seasons']

    show = {
        'title': title,
        'show_url': show_url,
        'year': year,
        'rating': rating,
        'seasons': seasons,
        'show_description': show_description
    }

    print(title)
    print()

    return show


def get_seasons_and_description(show_url):
    """
    Parameters
    ------
    show_url: string
        String for the current show url, to grab its page using requests

    Returns
    ------
    seasons_and_description: dict
        Dict containing:
        Description, and
        List containing 1 dict per season, containing:
        Season number,
        Season URL,
        1 list element per season, each containing:
        1 dict element per episode, each containing:
        Episode number, rating, number of ratings, name, date, description
    """

    connection_made = False
    while connection_made is False:
        try:
            page = requests.get(show_url)
        except requests.exceptions.ConnectionError:
            print("Connection refused.\nWaiting 60 seconds...")
            connection_made = False
            sleep(60)
        else:
            connection_made = True

    soup = BeautifulSoup(page.content.decode('utf8', 'ignore'), 'html.parser')

    show_description = soup.find('div', {'class': 'summary_text'}).contents[0]
    show_description = show_description.strip()
    if show_description == '':
        show_description = None

    div_seasons_nav = soup.find('div', {'class': 'seasons-and-year-nav'})
    if div_seasons_nav is not None:
        # Remove the first 2 divs which are column titles
        div_seasons_nav.div.decompose()
        div_seasons_nav.div.decompose()
        div_seasons = div_seasons_nav.div

        # Gets URLs for all seasons of each show
        # Note that these links are initially in reverse order
        a_season_links = div_seasons.find_all('a')
        season_urls = []
        for a in a_season_links:
            season_urls.append("https://www.imdb.com" + a["href"])
        season_urls.reverse()

        # Retrieve all episodes of each season
        seasons = []
        season_number = 1
        for season_url in season_urls:
            season_episodes = get_season_episodes(season_url)
            season = {
                'season_number': season_number,
                'season_url': season_url,
                'season_episodes': season_episodes
            }
            seasons.append(season)
            season_number = season_number + 1
    else:
        seasons = None

    seasons_and_description = {
        'show_description': show_description,
        'seasons': seasons
    }

    return seasons_and_description


def get_season_episodes(season_url):
    """
        Parameters
        ------
        season_url: string
            String for the current season url, to grab its page using requests

        Returns
        ------
        season_episodes: List
            List containing:
            1 dict element per episode, each containing:
            Episode name, link, airdate, rating, number of ratings, description
        """

    sleep(1)
    connection_made = False
    while connection_made is False:
        try:
            page = requests.get(season_url)
        except requests.exceptions.ConnectionError:
            print("Connection refused.\nWaiting 60 seconds...")
            connection_made = False
            sleep(60)
        else:
            connection_made = True

    soup = BeautifulSoup(page.content.decode('utf8', 'ignore'), 'html.parser')

    # Lambda is used to filter only relevant divs that contain episode information
    div_eplist = soup.find('div', {'class': 'list detail eplist'}).findChildren('div', {
        'class': lambda s: 'list_item odd' in s or 'list_item even' in s}, recursive=False)

    season_episodes = []
    print(season_url)
    ep_number = 1
    for div_list_item in div_eplist:
        div_info = div_list_item.find('div', {'class': 'info'})
        div_rating_widget = div_info.find('div', {'class': 'ipl-rating-widget'})
        if div_rating_widget is not None:
            div_rating = div_rating_widget.find('div',
                                                {'class': 'ipl-rating-star small'})
        else:
            div_rating = None

        if div_rating is not None:
            span_rating = div_rating.find('span', {
                'class': 'ipl-rating-star__rating'})
            if span_rating is not None:
                rating = span_rating.contents[0]
            else:
                rating = None

            span_totalvotes = div_rating.find('span', {
                'class': 'ipl-rating-star__total-votes'})
            if span_totalvotes is not None:
                totalvotes = span_totalvotes.contents[0]
                totalvotes = totalvotes.replace('(', '')
                totalvotes = totalvotes.replace(')', '')
            else:
                totalvotes = None
        else:
            rating = None
            totalvotes = None

        name = div_info.strong.a.contents[0]
        href = 'https://www.imdb.com' + div_info.strong.a['href']

        airdate = div_info.find('div', {'class': 'airdate'}).contents[0]
        airdate = airdate.strip()
        if airdate == '':
            airdate = None

        ep_description = div_info.find('div', {'class': 'item_description'}).contents[0]
        ep_description = ep_description.strip()
        if ep_description == 'Know what this is about?':
            ep_description = None

        print(name)
        print(airdate)
        print(rating)
        print(totalvotes)
        print(ep_description)

        episode = {
            'ep_number': ep_number,
            'name': name,
            'ep_url': href,
            'airdate': airdate,
            'rating': rating,
            'totalvotes': totalvotes,
            'ep_description': ep_description
        }
        season_episodes.append(episode)
        ep_number = ep_number + 1

    print()
    return season_episodes
