# Standard library imports
import csv


# Third-party imports


# Local application imports



class StampsImport:
    def __init__(self, file):
        self.file = file

    def read_csv(self):
        file_text = self.file.read().decode()
        csv_reader = csv.reader(file_text.splitlines(), delimiter=',')
        return csv_reader

    @property
    def stamp_list(self):
        csv_reader = self.read_csv()
        return [row[1] for row in csv_reader]