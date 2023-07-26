from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime
from lxml import etree

cities_canada = ["vancouver", "calgary", "edmonton", "saskatoon", "winnipeg", "toronto", "ottawa", "montreal", "halifax", "st-johns", "victoria", "regina", "hamilton", "london_ontario", "104045032964460", "windsor", "106063096092020", "114418101908145", "kingston-ca", "112068512144714", "115104881837942", "102170323157613", "111551465530472", "101877776521079", "111949595490847", "112008808810771", "110893392264912"]
canadian_cities_names = ["vancouver", "calgary", "edmonton", "saskatoon", "winnipeg", "toronto", "ottawa", "montreal", "halifax", "stjohns", "victoria", "regina", "hamilton", "london", "kitchener", "windsor", "stcatharines", "oshawa", "kingston", "fredericton", "charlottetown", "moncton", "thunderbay", "sudbury", "kelowna", "abbotsford", "barrie"]


def facebook_search(callback, manufacturer, model, yearLower, yearUpper):
    driver = webdriver.Chrome()
    callback("Starting facebook Canada search...")

    # Wipe the file clean with search information on each new line
    with open("./logs/facebook.csv", "w") as f:
        f.write(f"title,price,kilometers,date_posted,location,link\n")

    # Create an empty set to store unique car listings
    unique_listings = set()

    for city in cities_canada:
        # Restart driver every fifth search to prevent rate limiting
        # if cities_canada.index(city) % 5 == 0:
        #     callback("Restarting driver to prevent rate limiting...", "warning")
        #     driver.quit()
        #     driver = webdriver.Chrome()

        callback(f"Searching {canadian_cities_names[cities_canada.index(city)]}...")

        # Format the search query for the URL
        url = f"https://www.facebook.com/marketplace/{city}/vehicles?maxYear={yearUpper}&minYear={yearLower}&make=410067716491465&model=1120660268113320&transmissionType=automatic&exact=false"
        driver.get(url)

        # Wait for the search results to load
        callback("Waiting for all listings to load...")
        wait = WebDriverWait(driver, 10)
        #wait until the element with the attribute data-testid="SearchResultListItem" is present
        wait.until(EC.presence_of_element_located((By.ID, "seo_pivots")))

        # Get the page source and create a BeautifulSoup object
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Find all car listings on the search results page with xpath
        callback("Collecting listing data...")
        listing_selector = "a[href^='/marketplace/item/']"
        car_listings = soup.select(listing_selector)

        for car_listing in car_listings:
            # Extract the price, kilometers, title, and location
            meta_element = car_listing.find_all("span", attrs={"dir": "auto"})
            # Check for original price before reduction and remove it from the list
            if "$" in meta_element[1].text.strip():
                meta_element.pop(1)
            price = meta_element[0].text.strip()[1:] if meta_element else "N/A"

            title = meta_element[1].text.strip() if meta_element else "N/A"

            kilometers = f"{meta_element[3].text.strip()[:-4]},000" if meta_element else "N/A"

            location = meta_element[2].text.strip().split(",")[0] if meta_element else "N/A"

            # Extract the link using the "a" tag
            raw_link = car_listing.get("href").strip() if car_listing else "N/A"
            link_list = raw_link.split("?")
            formatted_link = f"https://www.facebook.com{link_list[0]}" if link_list else "N/A"

            # Generate a unique identifier for each car
            unique_id = f"{title}_{price}"

            # Check if the unique_id is already in the set, if not, process the car listing
            if unique_id not in unique_listings:
                unique_listings.add(unique_id)  # Add the unique_id to the set to mark it as processed

                # Write data to CSV
                with open("./logs/facebook.csv", "a", newline="", encoding="utf-8") as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([title, price, kilometers, "N/A", location, formatted_link])

        callback(f"Finished searching {canadian_cities_names[cities_canada.index(city)]}!")
        time.sleep(2) # Prevents rate limiting
    callback("Finished searching facebook! Output saved to ./logs/facebook.csv", "success")