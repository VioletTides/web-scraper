from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime


alberta = {
    "locations": ["calgary","edmonton","ftmcmurray","lethbridge","hat","peace","reddeer"]
}
british_columbia = {
    "locations": ["cariboo","comoxvalley","abbotsford","kamloops","kelowna","kootenays","nanaimo","princegeorge","skeena","sunshine","vancouver","victoria","whistler"]
}
manitoba = {
    "locations": ["winnipeg"]
}
new_brunswick = {
    "locations": ["newbrunswick"]
}
newfoundland_and_labrador = {
    "locations": ["newfoundland"]
}
northwest_territories = {
    "locations": ["territories","yellowknife"]
}
nova_scotia = {
    "locations": ["halifax"]
}
ontario = {
    "locations": ["barrie","belleville","brantford","chatham","cornwall","guelph","hamilton","kingston","kitchener","london","niagara","ottawa","owensound","peterborough","sarnia","soo","sudbury","thunderbay","toronto","windsor"]
}
pei = {
    "locations": ["pei"]
}
quebec = { # Common French L I can't get it to work work for french craigslist
    "locations": ["montreal","quebec","saguenay","sherbrooke","troisrivieres"]
} 
saskatchewan = {
    "locations": ["regina","saskatoon"]
}
yukon = {
    "locations": ["whitehorse"]
}

provinces = [alberta, british_columbia, manitoba, new_brunswick, newfoundland_and_labrador, northwest_territories, nova_scotia, ontario, pei, saskatchewan, yukon]
province_names = ["Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Northwest Territories", "Nova Scotia", "Ontario", "PEI", "Saskatchewan", "Yukon"]

def craigslist_search(callback, manufacturer, model, yearLower, yearUpper):
    driver = webdriver.Chrome()
    callback("Starting craigslist Canada search...")

    # Wipe the file clean with search information on each new line
    with open("./logs/craigslist.csv", "w") as f:
        f.write(f"title,price,kilometers,date_posted,location,link\n")

    # Create an empty set to store unique car listings
    unique_listings = set()

    for province in provinces:
        cities = province["locations"]
        for city in cities:
            callback(f"Searching {city}...")

            # Format the search query for the URL
            url = f"https://{city}.craigslist.org/search/cta?auto_make_model={manufacturer}%20miata&auto_transmission=2&max_auto_year={yearUpper}&min_auto_year={yearLower}"
            driver.get(url)

            # Wait for the search results to load
            callback("Waiting for all listings to load...")
            wait = WebDriverWait(driver, 10)
            #wait until the element with the attribute data-testid="SearchResultListItem" is present
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cl-results-page")))

            # Get the page source and create a BeautifulSoup object
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            # Find all car listings on the search results page
            callback("Collecting listing data...")
            car_listings = soup.find_all("li",class_="cl-search-result")

            for car_listing in car_listings:
                # Extract the listing title
                title_element = car_listing.find("span", class_="label")
                title = title_element.text.strip() if title_element else "N/A"

                # Extract the price
                price_element = car_listing.find("span", class_="priceinfo")
                price = price_element.text.strip() if price_element else "N/A"

                # Extract the date posted kilometers, and location from the metadata
                meta_element = car_listing.find("div", class_="meta")
                meta = meta_element.text.strip() if meta_element else "N/A"
                meta_list = meta.split("·")
                date = f"{meta_list[0]}/2023" if meta_list else "N/A"
                # Convert the date to DD/MM/YYYY format
                try:
                    date = datetime.strptime(date, "%m/%d/%Y")
                    date = date.strftime("%d/%m/%Y")
                except ValueError:
                    date = "Invalid Date"

                kilometers = meta_list[1][:-2] if len(meta_list) >= 2 else "N/A"

                location = meta_list[2] if len(meta_list) >= 3 else "N/A"

                # Extract the listing link
                link_element = car_listing.find("a", class_="cl-app-anchor")
                formatted_link = link_element.get("href") if link_element else "N/A"

                # Generate a unique identifier for each car
                unique_id = f"{title}_{price}"

                # Check if the unique_id is already in the set, if not, process the car listing
                if unique_id not in unique_listings:
                    unique_listings.add(unique_id)  # Add the unique_id to the set to mark it as processed

                    # Write data to CSV
                    with open("./logs/craigslist.csv", "a", newline="", encoding="utf-8") as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow([title, price, kilometers, date, location, formatted_link])

            callback(f"Finished searching {city}!")
            time.sleep(2) # Prevents rate limiting
        callback(f"Finsihed searching {province_names[provinces.index(province)]}!", "partial_success")
    callback("Finished searching craigslist! Output saved to ./logs/craigslist.csv", "success")