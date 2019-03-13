# tv-ratings-scrape
Right now this script scrapes info from the most popular shows of every genre on IMDB.

Requests and Beautiful Soup are the main dependencies, to access the web pages and navigate DOM elements.

The goal for this project is to feed into a React web app to display graphs depicting the variation in a show's perceived quality (its rating per episode) over time.

### How to use
Simply run scrape.py and the script will dump JSON files into a new directory (currently formatted for Windows filesystem).

## Example
The scraper follows this sort of url trail to get info from each show from each genre, starting from [this page](https://www.imdb.com/chart/tvmeter?ref_=nv_tvv_mptv):

![Screenshot 1](/docs/img/screen1.png)

![Screenshot 2](/docs/img/screen2.png)

![Screenshot 3](/docs/img/screen3.png)

![Screenshot 4](/docs/img/screen4.png)

## TODO / issues:
- Upload to MongoDB needs to be added
- Queue of 'files to upload' needs to be added
- Some special characters in titles need to be dealt with
- Shows without a release year need to be dealt with; detection exists