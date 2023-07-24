from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

def autotrader_search(driver, manufacturer, model, yearLower, yearUpper):
    print("Starting autotrader.ca search...")
    # Wipe the file clean with search information on each new line
    with open("./logs/autotrader.csv", "w") as f:
        f.write(f"title,price,kilometers,date_posted,link\n")

    # Open autotrader and search for the provided search query
    url = f"https://www.autotrader.ca/cars/{manufacturer}/miata%20mx-5/?rcp=15&rcs=0&srt=35&yRng={yearLower}%2C{yearUpper}&prx=-1&loc=l7l6t8&trans=Automatic&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch"
    driver.get(url)

    # Wait for the search results to load
    print("Waiting for all listings to load...")
    wait = WebDriverWait(driver, 10)
    #wait until the elements are present
    wait.until(EC.presence_of_element_located((By.ID, "SearchListings")))

    # Get the page source and create a BeautifulSoup object
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Get the page source and create a BeautifulSoup object
    print("Collecting listing data...")
    car_listings = soup.find_all("div", class_="result-item")
    
    # Wipe the file clean with search information on each new line
    with open("./logs/autotrader.csv", "w") as f:
        f.write(f"title,price,kilometers,date_posted,location,link\n")

    for car_listing in car_listings:
        # Extract the listing title
        title_element = car_listing.find("h2", class_="h2-title")
        title = title_element.text.strip() if title_element else "N/A"

        # Extract the price
        price_element = car_listing.find("span", class_="price-amount")
        price = price_element.text.strip() if price_element else "N/A"

        # Extract the kilometers
        kilometers_element = car_listing.find("span", class_="odometer-proximity")
        kilometers = kilometers_element.text.strip() if price_element else "N/A"

        # Extract the location
        location_element = car_listing.find("span", class_="proximity-text")
        location = location_element.text.strip() if location_element else "N/A"

        # Extract the link using the "a" attribute by xpath
        link_element = car_listing.find("a", class_="result-item-inner")
        raw_link = link_element.get("href") if link_element else "N/A"
        formatted_link = f"https://autotrader.ca{raw_link}"
        
        # Log the data to the file keeping spacing between each listing horizontally with ljust
        with open("./logs/autotrader.csv", "a", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([title,price,kilometers,"N/A",location,formatted_link])
    print("Done searching autotrader.ca!")