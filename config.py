# How many pages to scrape per genre; each page contains ~50 shows
PAGES_PER_GENRE = 5

# URL containing the list of URLS for genre pages
GENRE_LIST_URL = 'https://www.imdb.com/chart/tvmeter?ref_=nv_tvv_mptv'

# Seconds to wait when making a series of HTTP requests; this is to avoid being refused a connection
SHORT_WAIT = 1

# Seconds to wait after being refused a connection
LONG_WAIT = 45

# Days to wait until updating a show again
DAYS_TO_WAIT_BEFORE_UPDATE = 7

# Datetime format for writing to JSON; the default ISO 8601 format is currently preferred
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
