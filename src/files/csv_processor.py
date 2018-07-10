import csv
import os

class CsvProcessor(object):
    """
    Object that handles the writing/loading of CSV files.
    """

    def create_directory_structure(self, directory_path):
        """
        Creates the directory structure for the given path. Ignores all directory creation errors on purpose.
        """
        os.makedirs(directory_path)


    def map_to_csv(self, csv_file_path, function, **arguments):
        """
        Maps the given function to every row of the given CSV file.
        """
        if not os.path.exists(csv_file_path):
            return

        results = []
        with open(csv_file_path, mode="r", encoding="utf-8", newline="") as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            for row in reader:
                results.append(function(row, **arguments))
        return results


    def write_csv_row(self, csv_file_path, row):
        """
        Write a row to a given CSV file. Creates the file if non existant. Assumes directory existence.
        """
        try:
            with open(csv_file_path, mode="a", encoding="utf-8", newline="") as csv_file:
                writer = csv.writer(csv_file, delimiter=";")
                writer.writerow(row)
        except FileNotFoundError:
            print(f"[CsvFileProcessor] File not found error: '{csv_file_path}'.")


    def write_csv_rows(self, csv_file_path, rows):
        """
        Write a set of rows to a given CSV file. Creates the file if non existant. Assumes directory existence.
        """
        try:
            with open(csv_file_path, mode="a", encoding="utf-8", newline="") as csv_file:
                writer = csv.writer(csv_file, delimiter=";")
                for row in rows:
                    writer.writerow(row)
        except FileNotFoundError:
            print(f"[CsvFileProcessor] File not found error: '{csv_file_path}'.")
