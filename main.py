import websites.kijiji_autos as kijiji_autos
import websites.kijiji as kijiji
import websites.craigslist as craigslist
import websites.autotrader as autotrader
import websites.facebook as facebook
from utilities import combine_csv_files, chart_data
import tkinter as tk
import os
import customtkinter as ctk
import threading

def search_all_websites(callback, manufacturer, model, yearLower, yearUpper):
    # Define a list to store the threads
    threads = []

    # Function to start a website search in a separate thread
    def start_website_search(search_function):
        thread = threading.Thread(target=search_function, args=(callback, manufacturer, model, yearLower, yearUpper))
        threads.append(thread)
        thread.start()

    # Add all website search functions here
    start_website_search(kijiji.kijiji_search)
    start_website_search(kijiji_autos.kijiji_autos_search)
    start_website_search(autotrader.autotrader_search)
    start_website_search(craigslist.craigslist_search)
    start_website_search(facebook.facebook_search)

    # Wait for all threads to finish before continuing
    for thread in threads:
        thread.join()

    # All searches are complete
    callback("All website searches are complete!", "success")

# Getting input for car manufacturer, model, year, etc. (this doesn't work some website URLs are hardcoded lol)
manufacturer = "mazda"
model = "mx-5"
yearLower = "1990"
yearUpper = "1997"
# also automatic transmission but every website is different so no point in making a variable i don't care

input_files = ["./logs/kijiji.csv", "./logs/kijiji_autos.csv", "./logs/craigslist.csv", "./logs/autotrader.csv", "./logs/facebook.csv"]  # Replace with your actual file paths
output_file = "./logs/combined.csv"  # Replace with the desired output file path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("800x700")
app.title("Car Web Scraper")

# Main Frame
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill=ctk.BOTH, expand=True)

# Sidebar with title and buttons
sidebar = ctk.CTkFrame(main_frame, width=200)
sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
sidebar.pack_propagate(0)

# Search all button
search_all_button = ctk.CTkButton(sidebar, text="Search all", font=("Arial", 18), command=lambda: threading.Thread(target=search_all_websites, args=(callback, manufacturer, model, yearLower, yearUpper)).start())
search_all_button.pack(fill=tk.X, padx=10, pady=10)
search_all_button.pack_propagate(0)

# Search Kijiji button
kijiji_button = ctk.CTkButton(sidebar, text="Search Kijiji", font=("Arial", 18), command=lambda: threading.Thread(target=kijiji.kijiji_search, args=(callback, manufacturer, model, yearLower, yearUpper)).start())
kijiji_button.pack(fill=tk.X, padx=10, pady=10)
kijiji_button.pack_propagate(0)

# Search Kijiji Autos button
kijiji_autos_button = ctk.CTkButton(sidebar, text="Search Kijiji Autos", font=("Arial", 18), command=lambda: threading.Thread(target=kijiji_autos.kijiji_autos_search, args=(callback, manufacturer, model, yearLower, yearUpper)).start())
kijiji_autos_button.pack(fill=tk.X, padx=10, pady=10)
kijiji_autos_button.pack_propagate(0)

# Search Autotrader button
autotrader_button = ctk.CTkButton(sidebar, text="Search Autotrader", font=("Arial", 18), command=lambda: threading.Thread(target=autotrader.autotrader_search, args=(callback, manufacturer, model, yearLower, yearUpper)).start())
autotrader_button.pack(fill=tk.X, padx=10, pady=10)
autotrader_button.pack_propagate(0)

# Search Craigslist button
craigslist_button = ctk.CTkButton(sidebar, text="Search Craigslist", font=("Arial", 18), command=lambda: threading.Thread(target=craigslist.craigslist_search, args=(callback, manufacturer, model, yearLower, yearUpper)).start())
craigslist_button.pack(fill=tk.X, padx=10, pady=10)
craigslist_button.pack_propagate(0)

# Search Facebook button
facebook_button = ctk.CTkButton(sidebar, text="Search Facebook", font=("Arial", 18), command=lambda: threading.Thread(target=facebook.facebook_search, args=(callback, manufacturer, model, yearLower, yearUpper)).start())
facebook_button.pack(fill=tk.X, padx=10, pady=10)
facebook_button.pack_propagate(0)

# Combine CSVs button
combine_csvs_button = ctk.CTkButton(sidebar, text="Combine CSVs", font=("Arial", 18), command=lambda: threading.Thread(target=combine_csv_files, args=(callback, input_files, output_file)).start())
combine_csvs_button.pack(fill=tk.X, side=tk.TOP, padx=10, pady=10)
combine_csvs_button.pack_propagate(0)

# Plot data button
plot_data_button = ctk.CTkButton(sidebar, text="Plot data", font=("Arial", 18), command=lambda: threading.Thread(target=chart_data, args=(output_file,)).start())
plot_data_button.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
plot_data_button.pack_propagate(0)

# Open CSV log button
open_csv_button = ctk.CTkButton(sidebar, text="Open CSV log", font=("Arial", 18), command=lambda: threading.Thread(os.startfile(os.path.abspath("./logs/combined.csv"))).start())
open_csv_button.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
open_csv_button.pack_propagate(0)

# Right side with options panel and console log below

# Options panel
options_panel = ctk.CTkFrame(main_frame, height=150)
options_panel.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)
options_panel.pack_propagate(0)

# Title
title = ctk.CTkLabel(options_panel, text="Car Web Scraper", font=("Arial", 20))
title.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Car Manufacturer and Model on the same line
manufacturer_model_frame = ctk.CTkFrame(options_panel)
manufacturer_model_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

manufacturer_entry = ctk.CTkEntry(manufacturer_model_frame)
manufacturer_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
model_entry = ctk.CTkEntry(manufacturer_model_frame)
model_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Years on the next line
years_frame = ctk.CTkFrame(options_panel)
years_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

year_lower_entry = ctk.CTkEntry(years_frame)
year_lower_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

year_upper_entry = ctk.CTkEntry(years_frame)
year_upper_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

note_text = ctk.CTkLabel(options_panel, text="these fields don't work it's just to show the data lol", font=("Arial", 14))
note_text.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Set the default values in the input fields
manufacturer_entry.insert(0, manufacturer)
model_entry.insert(0, model)
year_lower_entry.insert(0, yearLower)
year_upper_entry.insert(0, yearUpper)

# Console log
console_log = ctk.CTkTextbox(main_frame)
console_log.configure(state="disabled")
console_log.pack(side=ctk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

def callback(message, colour="white"):
    console_log.configure(state="normal")  # Allows the textbox to be edited
    console_log.insert(tk.END, message + "\n", colour)  # Inserts the message into the textbox
    console_log.see(tk.END)  # Scrolls the textbox to the bottom
    console_log.configure(state="disabled")  # Disables the textbox so it can't be edited

console_log.tag_config("normal", foreground="white")
console_log.tag_config("success", foreground="green")
console_log.tag_config("partial_success", foreground = "blue")
console_log.tag_config("error", foreground="red")
console_log.tag_config("warning", foreground="orange")

app.mainloop()



# def get_data():
#     autotrader.autotrader_search(driver, manufacturer, model, yearLower, yearUpper)
#     kijiji.kijiji_search(driver, manufacturer, model, yearLower, yearUpper)
#     kijiji_autos.kijiji_autos_search(driver, manufacturer, model, yearLower, yearUpper)
#     craigslist.craigslist_search(driver, manufacturer, model, yearLower, yearUpper)

#     # Close the browser after scraping
#     driver.close()