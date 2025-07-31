import csv
import os
from pathlib import Path

def split(args):
    filenames = []
    if len(args.split_large_file) == 1 and args.split_large_file[0].endswith('/'):
        # If only one argument is a directory, upload all files in that directory
        directory = args.split_large_file[0]
        for filename in os.listdir(directory):
            full_path = os.path.join(directory, filename)
            if os.path.isfile(full_path):
                filenames.append(full_path)
    else:
        for filename in args.split_large_file:
            filenames.append(filename)

    for filename in filenames:
        if not filename.endswith('.csv'):
            print(f"Skipping {filename}, not a CSV file.")
            continue

        Path("../split_files").mkdir(parents=True, exist_ok=True)
        split_path = Path("../split_files")

        # Read the CSV file and split it into chunks of 10000 lines
        with open(filename, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)

            chunk = []
            file_index = 1

            for i, row in enumerate(reader, start=1):
                chunk.append(row)

                if len(chunk) == 10000:
                    split_filename = filename.split("/")[-1] + f"_{file_index}.csv"
                    with open(split_path / split_filename, mode='w', newline='', encoding='utf-8') as outfile:
                        writer = csv.writer(outfile)
                        writer.writerow(header)
                        writer.writerows(chunk)

                    print(f"Saved: {split_path / split_filename}")
                    file_index += 1
                    chunk = []

            # Handle leftover rows (if total rows not divisible by 10000)
            if chunk:
                split_filename = filename.split("/")[-1] + f"_{file_index}.csv"
                with open(split_path / split_filename, mode='w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(header)
                    writer.writerows(chunk)
                print(f"Saved: {split_path / split_filename}")
