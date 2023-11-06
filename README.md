# About

  

A web-scraper designed for scraping Indeed's UK website. Other examples of scraping indeed did not work properly for the UK version of the site so I built this to fulfill that niche.

## Table of Contents

  

    
- [Local Setup](#local-setup)
- [Technologies Used](#technologies-used)
- [Status](#status)
- [License](#license)

  

## Local Setup

  

This scraper uses ScrapeOps Proxy API to rotate proxies.

You can sign up for a free API Key Here

  

Add your API Key to the settings.py file like so:

  

This web scraper is setup to export the data as a timestamped CSV file.

  

Install the requirements, a python virtual enviroment is recommended.

  

`pip install requirements`

  

Run the spider

  

`scrapy indeedspider crawl`

  

## Technologies Used

  

## Status

Completed.

If I return to the project I plan to add:
- Item Class and Pipeline to clean the data returned
## Credits

Adapted from Scrapy Guidebook's Indeed scraper guide.

## License
This project is licensed under the MIT License.

