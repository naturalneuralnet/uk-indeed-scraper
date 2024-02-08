# About

A web-scraper designed for scraping Indeed's UK website. Other examples of scraping indeed did not work properly for the UK version of the site so I built this to fulfill that niche.

## Table of Contents

- [Local Setup](#local-setup)
- [Technologies Used](#technologies-used)
- [Status](#status)
- [License](#license)

## Local Setup

Clone or download the repository.

### ScrapeOps Proxy Config

This scraper uses ScrapeOps Proxy API to rotate proxies.

You can sign up for a free API Key at [scrapeops.io](https://scrapeops.io/app/proxy)

Add your API Key to the settings.py file at line 22.

```python
settings.py

SCRAPEOPS_API_KEY = 'YOUR_API_KEY_HERE'
```

This web scraper is setup to export the data as a timestamped CSV file with Scrapy's feed function. 

### Install Requirements

Install the requirements, a python virtual environment is recommended.

`pip install -r requirements.txt`

Run the spider

`scrapy indeedspider crawl`

## Technologies Used

- Python
- Scrapy
  
## Status

Completed.

If I return to the project I plan to add:
- Item Class and Pipeline to clean the data scraped data, specifically to strip the HTML tags from the job description.
## Credits

Adapted from Scrapy Guidebook's Indeed [scraping guide](https://thepythonscrapyplaybook.com/python-scrapy-indeed-scraper/#bypassing-indeeds-anti-bot-protection)

## License
This project is licensed under the MIT License.

You can find the License [here](LICENSE.md)