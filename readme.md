# tv-ratings-scrape
Currently, this python script scrapes information from the top 100 shows on IMDB and dumps the contents into a JSON file for each show.

Requests and Beautiful Soup are the main dependencies, to access the web pages and navigate DOM elements.

The goal for this project is to feed into a React web app to display graphs depicting the variation in a show's perceived quality (its rating per episode) over time.

### How to use
Simply run scrape.py and the script will dump JSON files into a new directory.