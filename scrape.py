import util_scrape

# Each genre in this list will be scraped for page_count # of pages
page_count = 10
genre_urls = util_scrape.get_list_of_genre_urls('https://www.imdb.com/chart/tvmeter?ref_=nv_tvv_mptv')
for url in genre_urls:
    print(url)
    util_scrape.scrape_shows_from_genre_pages(url, page_count)
