# COSC482-Assignment5
Scraping:
* The scraper.py file sets up a selenium webdriver to access the ebay tech deals then scrolls to the end of the page to ensure that all deals are loaded.
* After everything is loaded (ensured by WebDriverWait), all tech deal information is scraped from the site and added to the csv.
* Note that if the ebay_tech_deals.csv doesn't exist, it will create the file.

Cleaning:

