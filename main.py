from selenium import webdriver
import websites.kijiji_autos as kijiji_autos
import websites.kijiji as kijiji
import websites.craigslist as craigslist
import websites.autotrader as autotrader
from csv_combiner import combine_csv_files

input_files = ["./logs/kijiji.csv", "./logs/kijiji_autos.csv", "./logs/craigslist.csv", "./logs/autotrader.csv"]  # Replace with your actual file paths
output_file = "combined.csv"  # Replace with the desired output file path

def get_data():
    driver = webdriver.Chrome()

    # Getting input for car manufacturer, model, year, etc. (this doesn't work some website URLs are hardcoded lol)
    manufacturer = "mazda"
    model = "mx-5"
    yearLower = "1990"
    yearUpper = "1997"
    # also automatic transmission but every website is different so no point in making a variable i don't care

    kijiji_autos.kijiji_autos_search(driver, manufacturer, model, yearLower, yearUpper)
    kijiji.kijiji_search(driver, manufacturer, model, yearLower, yearUpper)
    # craigslist.craigslist_search(driver, manufacturer, model, yearLower, yearUpper)
    autotrader.autotrader_search(driver, manufacturer, model, yearLower, yearUpper)

    # Close the browser after scraping
    driver.close()

# get_data()
combine_csv_files(input_files, output_file)