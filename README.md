# Windows Spotlight Scraper
A simple scraper to get windows spotlight wallpepers from https://windows10spotlight.com

All downloaded wallpapers can be found inside the `%USERHOME%/Pictues/Windows Spotlight Scraper` directory.

## How to Use
In a terminal run `main.py` and use option `--count` (or `-c`) to specify the number of most recent wallpapers to scrape.
If option `--count` (or `-c`) is not specified then all available wallpapers will be scraped.

Examples: 

`main.py -c 100` will scrape the 100 most recent wallpapers.
 
 `main.py` will scrape all the available wallpapers.
