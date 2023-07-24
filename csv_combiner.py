import csv

def combine_csv_files(input_files, output_file):
    print("Combining CSV files...")

    # Hardcoded header for column names
    header = ["title", "price", "kilometers", "date_posted", "location", "link"]

    # Initialize a set to keep track of unique entries
    unique_entries = set()

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
    print("CSV files combined!")