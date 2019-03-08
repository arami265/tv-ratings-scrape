# tv-ratings-scrape
Right now this script scrapes info from the most popular shows of every genre on IMDB.

Requests and Beautiful Soup are the main dependencies, to access the web pages and navigate DOM elements.

The goal for this project is to feed into a React web app to display graphs depicting the variation in a show's perceived quality (its rating per episode) over time.

### How to use
Simply run scrape.py and the script will dump JSON files into a new directory (currently formatted for Windows filesystem).

## TODO / issues:
- Detecting changes to a show's info needs to be added
- Some special characters in titles need to be dealt with
- Shows without a release year need to be dealt with