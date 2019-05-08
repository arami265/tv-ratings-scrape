from time import sleep
import util_string
import util_requests
import util_files
import config
import operator
import datetime

# Wait time for reconnecting, in seconds
short_wait = config.SHORT_WAIT


def get_list_of_genre_urls(most_popular_url):
    soup = util_requests.get_soup_from_url(most_popular_url)

    li_subnav_items = soup.find_all('li', {'class': 'subnav_item_main'})

    genre_url_list = []
    for li in li_subnav_items:
        genre_url = li.a['href']
        genre_url_list.append('https://www.imdb.com' + genre_url)

    return genre_url_list


def scrape_shows_from_genre_pages(genre_url):
    # First the "next URL" is set to the initial genre URL to scrape
    global next_genre_url
    next_genre_url = genre_url

    for i in range(1, config.PAGES_PER_GENRE + 1):
        if next_genre_url is None:
            print('No more pages in this genre.')
        else:
            # Gets the list of shows from IMDB
            soup = util_requests.get_soup_from_url(next_genre_url)

            # Gets all the rows of the tbody containing all the shows
            div_lister_items = soup.find_all('div', {'class': 'lister-item-content'})

            # Extract title, year, rating, and IMDB link from each show
            i0 = 1
            for div in div_lister_items:
                title = div.h3.a.contents[0]
                title = util_string.make_alphanumeric_for_filename(title)
                span_year = div.h3.find("span", {'class': 'lister-item-year text-muted unbold'})
                if span_year is not None and len(span_year.contents) > 0:
                    year = span_year.contents[0]
                    year = util_string.get_year_from_span(year)
                else:
                    year = ''

                # If the year is null, ignore this file for now
                # Typically this is an upcoming show without any episodes
                if year == '':
                    print(title + ' skipped! Missing year info...')
                else:
                    file_path = util_files.get_show_file_path(title, year)
                    print(title)
                    print(file_path)
                    print('Page ' + str(i) + ' #' + str(i0))
                    i0 = i0 + 1

                    # If the show doesn't have a file, create one
                    if util_files.does_file_exist(file_path) is False:
                        show_data = get_show_dict_from_div(div)

                        util_files.write_new_file(file_path, show_data)
                        print('New file written.')
                        print()
                    else:
                        # Check if enough time has passed to check the show for changes
                        old_show_data = util_files.read_json_file(file_path)
                        time_last_updated = datetime.datetime.strptime(old_show_data['time_last_updated'],
                                                                       config.DATETIME_FORMAT)
                        time_delta = datetime.datetime.now() - time_last_updated

                        if time_delta.days >= config.DAYS_TO_WAIT_BEFORE_UPDATE:
                            # We will compare old/new objects to see if changes are made
                            new_show_data = get_show_dict_from_div(div)

                            # time_last_updated is removed for now because it is not
                            # a consideration for whether the data is changed
                            new_show_data_copy = new_show_data.copy()

                            new_show_data.pop('time_last_updated')
                            old_show_data.pop('time_last_updated')

                            # If there is no change between the current and new data
                            if operator.eq(old_show_data, new_show_data):
                                print('No change!')
                            else:
                                util_files.write_file(file_path, new_show_data_copy)
                                print('There was a change. File overwritten.')
                        else:
                            print("Show was recently updated! Skipping...")
                        print()

            print()
            a_next_page = soup.find('a', {'class': 'lister-page-next next-page'})
            if a_next_page is not None:
                next_page_href = soup.find('a', {'class': 'lister-page-next next-page'})['href']
                next_genre_url = 'https://www.imdb.com' + next_page_href
            else:
                next_genre_url = None


def get_show_dict_from_div(div):
    print('get_show_dict_from_div')
    title = div.h3.a.contents[0]
    href = div.h3.a["href"]

    span_year = div.h3.find("span", {'class': 'lister-item-year text-muted unbold'})
    if span_year is not None and len(span_year.contents) > 0:
        year = span_year.contents[0]
        year = year.replace('(', '')
        year = year.replace(')', '')
        year = year[0:4]
    else:
        year = ''

    div_rating = div.find('div', {'class': 'inline-block ratings-imdb-rating'})
    if div_rating is not None:
        rating = div_rating.strong.contents[0]
    else:
        rating = None

    p_num_votes = div.find('p', {'class': 'sort-num_votes-visible'})
    if p_num_votes is not None:
        votes = p_num_votes.find('span', {'name': 'nv'}).contents[0]
    else:
        votes = None

    # Get all episodes from the current show
    show_url = 'https://www.imdb.com' + href
    seasons_and_description = get_seasons_and_description(show_url)

    show_description = seasons_and_description['show_description']
    seasons = seasons_and_description['seasons']

    if year == '':
        year = None

    time_last_updated = datetime.datetime.now().strftime(config.DATETIME_FORMAT)

    show = {
        'title': title,
        'show_url': show_url,
        'year': year,
        'rating': rating,
        'votes': votes,
        'seasons': seasons,
        'show_description': show_description,
        'time_last_updated': time_last_updated
    }

    return show


# def scrape_shows_from_top_100():
#     # Gets the most popular TV shows from IMDB
#     soup = util_requests.get_soup_from_url("https://www.imdb.com/chart/tvmeter?ref_=nv_tvv_mptv")
#
#     # Gets all the rows of the tbody containing all the shows
#     tr_show_items = soup.find('tbody', {'class': 'lister-list'}).findChildren('tr', recursive=False)
#
#     # Extract title, year, rating, and IMDB link from each show
#     for tr in tr_show_items:
#         show = get_show_dict_from_tr(tr)
#
#         title = util_string.make_alphanumeric_for_filename(show['title'])
#         file_name = '.\\shows\\' + title + '_' + show['year'] + '.json'
#
#         with open(file_name, 'w') as outfile:
#             json.dump(show, outfile)
#
#
# def get_show_dict_from_tr(tr):
#     """
#     Receives an IMDB page with a list of shows and returns a dict
#     :param tr:
#     :return:
#     Returns a dict with the show's information
#     """
#     title_column = tr.find('td', {'class': 'titleColumn'})
#     title = title_column.a.contents[0]
#     href = title_column.a["href"]
#     year = title_column.span.contents[0]
#     year = year.replace('(', '')
#     year = year.replace(')', '')
#
#     rating_column = tr.find('td', {'class': 'ratingColumn imdbRating'})
#     if rating_column.strong is not None:
#         rating = rating_column.strong.contents[0]
#     else:
#         rating = None
#
#     # Get all episodes from the current show
#     show_url = 'https://www.imdb.com' + href
#     seasons_and_description = get_seasons_and_description(show_url)
#
#     show_description = seasons_and_description['show_description']
#     seasons = seasons_and_description['seasons']
#
#     show = {
#         'title': title,
#         'show_url': show_url,
#         'year': year,
#         'rating': rating,
#         'seasons': seasons,
#         'show_description': show_description
#     }
#
#     print(title)
#     print()
#
#     return show


def get_seasons_and_description(show_url):
    print('get_seasons_and_description')
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

    sleep(short_wait)
    soup = util_requests.get_soup_from_url(show_url)

    div_description = soup.find('div', {'class': 'summary_text'})
    if div_description is not None:
        show_description = div_description.contents[0]
        show_description = show_description.strip()
        if show_description == '':
            show_description = None
    else:
        show_description = None

    div_seasons_nav = soup.find('div', {'class': 'seasons-and-year-nav'})
    div_no_season = soup.find_all('div', {'class': 'no-season'})

    if div_seasons_nav is not None and len(div_no_season) == 0:
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
    # Deal with shows such as https://www.imdb.com/title/tt0388629/?ref_=adv_li_tt
    # which have years but no seasons on their page
    #
    # elif div_seasons_nav is not None and div_no_season is not None:
    #     div_no_season = div_no_season.pop(0)
    #     a_years = div_no_season.find_all('a')
    #
    #     if a_years is not None:
    #         a_years.reverse()
    #
    #         if a_years[0].contents[0] == '… See all':
    #             print('No seasons show detected!')
    else:
        seasons = None

    seasons_and_description = {
        'show_description': show_description,
        'seasons': seasons
    }

    return seasons_and_description


def get_season_episodes(season_url):
    print('get_season_episodes')
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

    sleep(short_wait)
    soup = util_requests.get_soup_from_url(season_url)

    # Lambda is used to filter only relevant divs that contain episode information
    div_eplist = soup.find('div', {'class': 'list detail eplist'})
    if div_eplist is None:
        season_episodes = None
    else:
        div_list_items = div_eplist.findChildren('div', {
            'class': lambda s: 'list_item odd' in s or 'list_item even' in s}, recursive=False)

        season_episodes = []
        print(season_url)
        ep_number = 1
        for div_list_item in div_list_items:
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

            # print(name)
            # print(airdate)
            # print(rating)
            # print(totalvotes)
            # print(ep_description)

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
