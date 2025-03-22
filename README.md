# COSC482-Assignment5
## Scraping:
* The scraper.py file sets up a selenium webdriver to access the ebay tech deals then scrolls to the end of the page to ensure that all deals are loaded.
* After everything is loaded (ensured by WebDriverWait), all tech deal information is scraped from the site and added to the csv.
* Note that if the ebay_tech_deals.csv file doesn't exist, it will create the file.

## Cleaning:
* The clean_data.py file is used to clean the data in the ebay_tech_deals.csv file.
* It ensures the price and original_price values are numerical, non-null values.
* As an extra touch, I added code to ensure the original_price (price before discount) is never less than the price. If found to be less than it would be changed to the price.
* Also if missing the original_price would be put as equal to the price.
* In case the shipping information is unavailable, it would replace it with the message "Shipping info unavailable".

## EDA
* The key results of the analysis conducted on the cleaned data are as follows:
  - ### Time series analysis: ###
    There are about 100 tech deals being displayed on ebay per hour. Note that initially the number of deals was way higher than 100.
  - ### Price and discount analysis: ###
    - By looking at the distribution of prices, one can tell that the majority of the deals have a price between 0 and 400 dollars.
    - By looking at the original price vs price scatter plot, we can see that all tech deals either have  a price equal to the original or a price less than the original.
    - By looking at the discount percentage disribution, we can see that a lot of deals have no discounts, however from those that do, they commonly have a discount percentage between 40 and 70 percent.
  - ### Shipping Information analysis: ###
    Majority of the deals don't have any shipping information available but about 500 of the deals mention free shipping.
  - ### Text Analysis on Product Titles: ###
    Given the set of keywords "Laptop", "Phone", "Tablet", "Apple", "Samsung", "Xbox", the most frequent keywords were "Apple" and "Phone". On the other hand, the least frequent were "Tablet" and "Xbox". 
  - ### Price difference analysis: ###
    A lot of deals have a difference of 0 but some a difference wothe most frequent difference being around 200 dollars.
  - ### Discount: ###
    The top 5 seem to be the same deal just scraped at different times with a discount of 87.25%.

## Challenges

## Improvements
  
