import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import re

def parse_date_time(date_posted_str):
    if "<" in date_posted_str and "hours ago" in date_posted_str:
        # Handle "X hours ago" format
        hours_ago = int(re.search(r"\d+", date_posted_str).group())
        date_posted = datetime.now() - timedelta(hours=hours_ago)
    elif "weeks ago" in date_posted_str:
        # Handle "X weeks ago" format
        weeks_ago = int(re.search(r"\d+", date_posted_str).group())
        date_posted = datetime.now() - timedelta(weeks=weeks_ago)
    elif "days ago" in date_posted_str:
        # Handle "X days ago" format
        days_ago = int(re.search(r"\d+", date_posted_str).group())
        date_posted = datetime.now() - timedelta(days=days_ago)
    elif "months ago" in date_posted_str:
        # Handle "X months ago" format
        months_ago = int(re.search(r"\d+", date_posted_str).group())
        # Note: Using 30 days approximation for a month
        date_posted = datetime.now() - timedelta(days=months_ago * 30)
    else:
        try:
            # Try to parse the date using the format '%d/%m/%Y'
            date_posted = datetime.strptime(date_posted_str, "%d/%m/%Y")
        except ValueError:
            # If the above format fails, handle special cases like "a week ago," "a day ago," "a month ago," etc.
            if "a week ago" in date_posted_str:
                date_posted = datetime.now() - timedelta(weeks=1)
            elif "a day ago" in date_posted_str:
                date_posted = datetime.now() - timedelta(days=1)
            elif "a month ago" in date_posted_str:
                # Note: Using 30 days approximation for a month
                date_posted = datetime.now() - timedelta(days=30)
            else:
                # If none of the formats match, set the date_posted to None or raise an error as needed
                date_posted = None

    return date_posted

def chart_data(csv_file_path):
    # Lists to store data from the CSV file
    prices = []
    kilometers = []

    # Read data from the CSV file
    with open(csv_file_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            title, price_str, kilometers_str, date_posted_str, location, link = row

            # Convert price and kilometers strings to floats if possible
            try:
                price = float(price_str.replace(",", ""))
                kilometer = float(kilometers_str.replace(",", ""))
            except ValueError:
                continue

            prices.append(price)
            kilometers.append(kilometer)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.scatter(kilometers, prices, marker="o", alpha=0.5)
    plt.xlabel("Kilometers")
    plt.ylabel("Price ($)")
    plt.title("Price vs. Kilometers")
    plt.grid(True)
    plt.tight_layout()

    # Show the plot
    plt.show()

def combine_csv_files(callback, input_files, output_file):
    callback("Combining CSV files...")

    # Hardcoded header for column names
    header = ["title", "price", "kilometers", "date_posted", "location", "link"]

    # Initialize a set to keep track of unique entries
    unique_entries = set()

    try:
        # Open the output file for writing
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile_out:
            csv_writer = csv.writer(csvfile_out)

            # Write the header to the output file
            csv_writer.writerow(header)

            for file in input_files:
                # Open each input CSV file for reading
                with open(file, "r", newline="", encoding="utf-8") as csvfile_in:
                    csv_reader = csv.reader(csvfile_in)

                    # Skip the header row if it exists
                    next(csv_reader)

                    for row in csv_reader:
                        # Extract the title and link to create a unique identifier
                        title, link = row[0], row[5]
                        unique_id = f"{title}_{link}"

                        # Check if the entry is already in the set, if not, write it to the output file
                        if unique_id not in unique_entries:
                            unique_entries.add(unique_id)  # Add the unique entry to the set to mark it as processed
                            csv_writer.writerow(row)
    except:
        
    callback("CSV files combined! Output saved to ./logs/combined.csv", "success")