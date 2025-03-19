from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


def setup_driver():
    # Set up Selenium options
    options = Options()
    # Enable headless mode for GitHub Actions
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Rotate User-Agent to prevent detection
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")

    # Set up ChromeDriver using webdriver_manager
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


if __name__ == "__main__":
    driver = setup_driver()
    URL = "https://www.ebay.com/globaldeals/tech"

    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Stop scrolling when no new content is loaded
        last_height = new_height

    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "ebayui-refit-main-wrapper")))

    data = []

    try:
        items = driver.find_elements(By.CLASS_NAME, "dne-itemtile-detail")
        for item in items:
            try:
                title = item.find_element(
                    By.CLASS_NAME, "dne-itemtile-title").get_attribute('title')
            except:
                title = "N/A"
            try:
                price = item.find_element(
                    By.XPATH, './/span[@itemprop="price"]').text
            except:
                price = "N/A"
            try:
                original_price = item.find_element(
                    By.XPATH, './/div[@class="dne-itemtile-original-price"]/span/span').text
            except:
                original_price = "N/A"
            try:
                item_url = item.find_element(
                    By.XPATH, ".//a[@itemprop='url']").get_attribute("href")
            except:
                item_url = "N/A"
            try:
                shipping = item.find_element(
                    By.CLASS_NAME, "dne-itemtile-delivery").text
            except:
                shipping = "N/A"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data.append({"title": title, "price": price, "original_price": original_price,
                        "item_url": item_url, "shipping": shipping, "timestamp": timestamp})
    except:
        print("failed to find the tech items")
        
    file_name ="ebay_tech_deals.csv"
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "title", "price", "original_price", "item_url",
            "shipping", "timestamp"
        ])
    
    data_df= pd.DataFrame(data)
    df = pd.concat([df, data_df], ignore_index=True)
    
    # Save back to CSV
    df.to_csv(file_name, index=False)
