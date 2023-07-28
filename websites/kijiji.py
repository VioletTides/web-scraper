from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import csv
from utilities import parse_date_time

def kijiji_search(callback, manufacturer, model, yearLower, yearUpper):
    callback("Starting Kijiji search...", "normal")
    driver = webdriver.Chrome()

    # Format the search query for the URL
    formatted_query = f"{manufacturer}-mx5miata-{yearLower}__{yearUpper}/c174l0a54a1000054a68?transmission=2"

    # Open Kijiji and search for the provided search query
    url = f"https://www.kijiji.ca/b-cars-trucks/canada/{formatted_query}"
    driver.get(url)

    # Wait for the search results to load
    callback("Waiting for all listings to load...", "normal")
    wait = WebDriverWait(driver, 10)
    #wait until the elements are present
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".search-item")))

    # Get the page source and create a BeautifulSoup object
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Get the page source and create a BeautifulSoup object
    callback("Collecting listing data...", "normal")
    car_listings = soup.find_all("div", class_="search-item")
    
    # Wipe the file clean with search information on each new line
    with open("./logs/kijiji.csv", "w") as f:
        f.write(f"title,price,kilometers,date_posted,location,link\n")
    
    for car_listing in car_listings:
        # Extract the listing title
        title_element = car_listing.find("a", class_="title")
        title = title_element.text.strip() if title_element else "N/A"

        # Extract the price
        price_element = car_listing.find("div", class_="price")
        price = price_element.text.strip()[1:] if price_element else "N/A"

        # Extract the date posted
        date_element = car_listing.find("span", class_="date-posted")
        date = date_element.text.strip() if date_element else "N/A"
        date = parse_date_time(date)

        # Extract the kilometers
        kilometers_element = car_listing.find("div", class_="details")
        kilometers = kilometers_element.text.strip() if price_element else "N/A"
        kilometers_list = re.findall('\d+', kilometers)
        formatted_kilometers = f"{kilometers_list[0]},{kilometers_list[1]}" # This will fuck up if there are less than 1,000 kilometers but be real no miata has under 80k

        # Extract the location
        location_element = car_listing.find("div", class_="location")
        location = location_element.text.strip().replace("\n", "")[:-10].strip() if location_element else "N/A" # Weird bs where there was a bunch of whitespace and garbage I had to clean

        # Extract the link using the "a" attribute by xpath
        link_element = car_listing.find("a", class_="title")
        raw_link = link_element.get("href") if link_element else "N/A"
        formatted_link = f"https://kijiji.ca{raw_link}"
        
        # Log the data to the file keeping spacing between each listing horizontally with ljust
        with open("./logs/kijiji.csv", "a", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([title,price,formatted_kilometers,date,location,formatted_link])
    driver.quit()
    callback("Done searching Kijiji.ca! Output saved to ./logs/kijiji.csv", "success")