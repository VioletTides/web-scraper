from selenium import webdriver


import kijiji_autos

driver = webdriver.Chrome()

# Getting input for car manufacturer, model, year, etc.
manufacturer = "mazda"
model = "mx-5"
yearLower = "1990"
yearUpper = "1997"

kijiji_autos.kijiji_autos_search(driver, manufacturer, model, yearLower, yearUpper)

# Close the browser after scraping
driver.close()