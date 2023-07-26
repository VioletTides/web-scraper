from selenium import webdriver
import websites.kijiji_autos as kijiji_autos
import websites.kijiji as kijiji
import websites.craigslist as craigslist
import websites.autotrader as autotrader
import websites.facebook as facebook
from csv_combiner import combine_csv_files
import time
import tkinter as tk
import customtkinter as ctk
import threading

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
app.geometry("800x500")
app.title("Car Web Scraper")

# Main Frame
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill=ctk.BOTH, expand=True)

# Sidebar with title and buttons
sidebar = ctk.CTkFrame(main_frame, width=200)
sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
sidebar.pack_propagate(0)

# Title
title = ctk.CTkLabel(sidebar, text="Car Web Scraper", font=("Arial", 20))
title.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

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

# Combine CSVs button with bigger text and green button
combine_csvs_button = ctk.CTkButton(sidebar, text="Combine CSVs", font=("Arial", 18), command=lambda: threading.Thread(target=combine_csv_files, args=(callback, input_files, output_file)).start())
combine_csvs_button.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
combine_csvs_button.pack_propagate(0)

# Console log
console_log = ctk.CTkTextbox(main_frame, width=600, height=400)
console_log.configure(state="disabled")
console_log.pack(side=ctk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

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