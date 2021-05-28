# Project 3: Engineering - Product Drops Tracker
## Get push notifictions for products you're interested in

The goal of this project is to set up an push notification system for in demend products purchased online from vendors such as [Best Buy](https://bestbuy.com) and [Newegg](https://newegg.com/).
### Data
 * **acquisition**: web scraping, executed every 1-2 minute
 * **storage**: PostgreSQL
 * **sources**:
    - [Best Buy](https://bestbuy.com)
    - [Newegg](https://newegg.com/)
### Tools:
 - Web Scraping
    - `BeautifulSoup`, `Selenium`, `urlopen`
 - EDA & Data Cleanup
    - `Pandas`, `Jupyter Notebooks`
 - Push notifications
    - `Discord`
 - Task Sceduling
    - `Cron`