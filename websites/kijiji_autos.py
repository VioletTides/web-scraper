from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import csv

# TODO figure out a way to scrape dates as they aren't easily accessible like normal kijiji

def kijiji_autos_search(callback, manufacturer, model, yearLower, yearUpper):
    driver = webdriver.Chrome()
    callback("Starting Kijiji Autos search...")

    # Format the search query for the URL
    formatted_query = f"{manufacturer}/{model}/#tr=AUTOMATIC_GEAR&yc={yearLower}%3A{yearUpper}"

    # Open Kijiji Autos and search for the provided search query
    url = f"https://www.kijijiautos.ca/cars/{formatted_query}"
    driver.get(url)

    # Wait for the search results to load
    callback("Waiting for all listings to load...")
    wait = WebDriverWait(driver, 20)
    #wait until the element with the attribute data-testid="SearchResultListItem" is present
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='SearchResultListItem']")))

    # Move the mouse to hover over each "article" element to trigger the href to load
    articles = driver.find_elements(By.TAG_NAME, "article")
    callback("Hovering over element...")
    for article in articles:
        ActionChains(driver).move_to_element(article).perform()

    # Get the page source and create a BeautifulSoup object
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Find all car listings on the search results page
    callback("Collecting listing data...")
    car_listings = soup.find_all(attrs={"data-testid": "SearchResultListItem"})

    # Wipe the file clean with search information on each new line
    with open("./logs/kijiji_autos.csv", "w") as f:
        f.write("title,price,kilometers,date_posted,location,link\n")
    
    # Extract relevant information from each car listing
    for car_listing in car_listings:
        # Extract the title using the <h2> tag
        title_element = car_listing.find("h2")
        title = title_element.text.strip() if title_element else "N/A"

        # Extract the price using the specific data-testid attribute
        price_element = car_listing.find("div", attrs={"data-testid": "VehicleListItem-price"})
        price = price_element.text.strip() if price_element else "N/A"
        
        # Extract the kilometers and location using data-testid
        meta = car_listing.find_all("span", attrs={"data-testid": "VehicleListItemAttributeValue"})
        kilometers_element = meta[0]
        kilometers = kilometers_element.text.strip() if kilometers_element else "N/A"
        kilometers = kilometers[:-3] # Only keeps the number (with commas) by removing KM and some weirdo icon character
        
        location_element = meta[1]
        location = location_element.text.strip().split(",")[0] if location_element else "Invalid Location"
        if location == "-":
            location = "Invalid Location"
        
        # Extract the link using the "a" attribute by xpath
        link_element = car_listing.find("a")
        raw_link = link_element.get("href") if link_element else "N/A"
        # Clean the link to only include numbers
        link = "".join(filter(str.isdigit, raw_link))
        formatted_link = f"https://www.kijijiautos.ca/cars/{manufacturer}/{model}/#vip={link}"

        # Log the data to the file keeping spacing between each listing horizontally with ljust
        with open("./logs/kijiji_autos.csv", "a", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([title,price,kilometers,"N/A",location,formatted_link])
    driver.quit()
    callback("Done searching kijijiautos.ca! Output saved to ./logs/kijiji_autos.csv", "success")
