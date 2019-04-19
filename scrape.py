import util_scrape
import config

# Each genre in this list will be scraped for page_count # of pages
pages_per_genre = config.PAGES_PER_GENRE
genre_urls = util_scrape.get_list_of_genre_urls(config.GENRE_LIST_URL)
i = 1
for url in genre_urls:
    print('Genre ' + str(i) + '/' + str(len(genre_urls)))
    print(url)
    util_scrape.scrape_shows_from_genre_pages(url)
    i = i + 1
