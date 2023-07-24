from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

def kijiji_autos_search(driver, manufacturer, model, yearLower, yearUpper):
    # Format the search query for the URL
    formatted_query = f"{manufacturer}/{model}/#tr=AUTOMATIC_GEAR&yc={yearLower}%3A{yearUpper}"

    # Open Kijiji Autos and search for the provided search query
    url = f"https://www.kijijiautos.ca/cars/{formatted_query}"
    driver.get(url)

    # Wait for the search results to load
    wait = WebDriverWait(driver, 5)
    #wait until the element with the attribute data-testid="SearchResultListItem" is present
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='SearchResultListItem']")))

    # Move the mouse to hover over each "article" element to trigger the href to load
    articles = driver.find_elements(By.TAG_NAME, "article")
    print("Hovering over element")
    for article in articles:
        ActionChains(driver).move_to_element(article).perform()

    # Get the page source and create a BeautifulSoup object
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Find all car listings on the search results page
    car_listings = soup.find_all(attrs={"data-testid": "SearchResultListItem"})

    # Wipe the file clean with search information on each new line
    with open("kijiji_autos.txt", "w") as f:
        f.write(f"Search: {manufacturer} {model} {yearLower}-{yearUpper} automatic\n\n")
    
    # Extract relevant information from each car listing
    for car_listing in car_listings:
        # Extract the title using the <h2> tag
        title_element = car_listing.find("h2")
        title = title_element.text.strip() if title_element else "N/A"

        # Extract the price using the specific data-testid attribute
        price_element = car_listing.find("div", attrs={"data-testid": "VehicleListItem-price"})
        price = price_element.text.strip() if price_element else "N/A"

        # Extract the link using the "a" attribute by xpath
        link_element = car_listing.find("a")
        raw_link = link_element.get("href") if link_element else "N/A"
        # Clean the link to only include numbers
        link = "".join(filter(str.isdigit, raw_link))
        url = f"https://www.kijijiautos.ca/cars/{manufacturer}/{model}/#vip={link}"

        # Log the data to the file keeping spacing between each listing horizontally with ljust
        with open("kijiji_autos.txt", "a") as f:
            f.write(f"Title: {title.ljust(50)} Price: {price.ljust(20)} Link: {url}\n")


        print(f"Title: {title}, Price: {price}, Link: {url}\n")
